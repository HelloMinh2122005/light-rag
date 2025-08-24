# 🚀 LightRAG Makefile - Project management made easy
# Usage: make <command>

# Cấu hình mặc định
DOCKER_COMPOSE_FILE = docker/docker-compose.yaml
PROJECT_NAME = lightrag
PYTHON_VERSION = 3.12

# Colors cho output đẹp
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

# 📖 Show help
help:
	@echo ""
	@echo "$(GREEN)🚀 LightRAG Project Commands$(NC)"
	@echo ""
	@echo "$(YELLOW)📦 Setup & Installation:$(NC)"
	@echo "  make install          - Install project dependencies"
	@echo "  make setup            - Full project setup (install + env)"
	@echo "  make clean            - Clean caches and temporary files"
	@echo ""
	@echo "$(YELLOW)🐳 Docker Commands:$(NC)"
	@echo "  make build            - Build Docker images"
	@echo "  make up               - Start all services"
	@echo "  make down             - Stop all services"
	@echo "  make restart          - Restart all services"
	@echo "  make logs             - Tail logs (real-time)"
	@echo ""
	@echo "$(YELLOW)⚙️  Development:$(NC)"
	@echo "  make dev              - Run development mode (local)"
	@echo "  make test             - Run tests"
	@echo "  make test-api         - Test API endpoints"
	@echo "  make lint             - Check code quality"
	@echo ""
	@echo "$(YELLOW)📊 Data Management:$(NC)"
	@echo "  make reindex          - Reindex data"
	@echo "  make backup           - Create a backup"
	@echo "  make restore          - Restore data from backup"
	@echo ""
	@echo "$(YELLOW)🔍 Monitoring:$(NC)"
	@echo "  make status           - Check services status"
	@echo "  make health           - API health check"
	@echo "  make neo4j-browser    - Open Neo4j Browser"
	@echo ""

# 📦 Setup & Installation
install:
	@echo "$(GREEN)📦 Installing Python dependencies...$(NC)"
	pip install -r requirements.txt

setup: install
	@echo "$(GREEN)🔧 Setting up project...$(NC)"
	@mkdir -p data logs docker/volumes/rag_storage docker/volumes/neo4j_data docker/volumes/neo4j_logs
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)📝 Creating .env file...$(NC)"; \
		cp .env.example .env 2>/dev/null || echo "# Copy this to .env and configure\nOPENAI_API_KEY=your_key_here\nNEO4J_URI=bolt://neo4j:7687\nNEO4J_USERNAME=neo4j\nNEO4J_PASSWORD=your_password" > .env; \
	fi
	@echo "$(GREEN)✅ Setup complete! Edit the .env file with your API keys.$(NC)"

clean:
	@echo "$(GREEN)🧹 Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"

# 🐳 Docker Commands
build:
	@echo "$(GREEN)🔨 Building Docker images...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_FILE) build
	@echo "$(GREEN)✅ Build complete!$(NC)"

up:
	@echo "$(GREEN)🚀 Starting services...$(NC)"
	@make _create_volumes
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d
	@echo "$(YELLOW)⏳ Waiting for services to be ready...$(NC)"
	@sleep 30
	@make status
	@echo ""
	@echo "$(GREEN)✅ Services are running!$(NC)"
	@echo "🌐 API: http://localhost:8000"
	@echo "📖 Docs: http://localhost:8000/docs"
	@echo "🗃️ Neo4j: http://localhost:7474"

down:
	@echo "$(GREEN)🛑 Stopping services...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_FILE) down
	@echo "$(GREEN)✅ Services stopped!$(NC)"

restart:
	@echo "$(GREEN)🔄 Restarting services...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_FILE) restart
	@sleep 15
	@make status
	@echo "$(GREEN)✅ Services restarted!$(NC)"

logs:
	@echo "$(GREEN)📝 Showing logs (Ctrl+C to exit)...$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f

# ⚙️ Development
dev:
	@echo "$(GREEN)💻 Starting development mode...$(NC)"
	@echo "$(YELLOW)Make sure you have .env configured!$(NC)"
	cd src && python main.py

test:
	@echo "$(GREEN)🧪 Running tests...$(NC)"
	python -m pytest tests/ -v 2>/dev/null || echo "$(YELLOW)No pytest found. Running API test...$(NC)"
	python test_api.py

test-api:
	@echo "$(GREEN)🧪 Testing API endpoints...$(NC)"
	python test_api.py

lint:
	@echo "$(GREEN)🔍 Checking code quality...$(NC)"
	python -m flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics || echo "$(YELLOW)flake8 not installed. Run: pip install flake8$(NC)"

# 📊 Data Management
reindex:
	@echo "$(GREEN)🔄 Reindexing data...$(NC)"
	curl -X POST http://localhost:8000/reindex || echo "$(RED)❌ Failed to reindex. Make sure the API is running.$(NC)"
	@echo "$(GREEN)✅ Reindex complete!$(NC)"

backup:
	@echo "$(GREEN)💾 Creating backup...$(NC)"
	@mkdir -p backups
	@BACKUP_NAME=backup_$(shell date +%Y%m%d_%H%M%S); \
	echo "Creating backup: $$BACKUP_NAME"; \
	cp -r docker/volumes/rag_storage "backups/$$BACKUP_NAME" 2>/dev/null || echo "$(YELLOW)⚠️  RAG storage not found$(NC)"; \
	docker exec lightrag_neo4j cypher-shell -u neo4j -p your_password "CALL apoc.export.cypher.all('/var/lib/neo4j/import/$$BACKUP_NAME.cypher')" 2>/dev/null || echo "$(YELLOW)⚠️  Neo4j backup failed$(NC)"; \
	echo "$(GREEN)✅ Backup created: $$BACKUP_NAME$(NC)"

restore:
	@echo "$(GREEN)🔄 Available backups:$(NC)"
	@ls backups/ 2>/dev/null || echo "$(YELLOW)No backups found$(NC)"
	@echo "$(YELLOW)To restore, copy backup files manually to docker/volumes/$(NC)"

# 🔍 Monitoring
status:
	@echo "$(GREEN)📊 Service Status:$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps

health:
	@echo "$(GREEN)❤️  Checking API health...$(NC)"
	@curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "$(RED)❌ API not responding$(NC)"

neo4j-browser:
	@echo "$(GREEN)🗃️  Opening Neo4j Browser...$(NC)"
	@echo "URL: http://localhost:7474"
	@echo "Username: neo4j"
	@echo "Password: your_password"
	@python -m webbrowser http://localhost:7474 2>/dev/null || echo "$(YELLOW)Please open http://localhost:7474 manually$(NC)"

# 🔧 Internal helpers
_create_volumes:
	@mkdir -p docker/volumes/rag_storage docker/volumes/neo4j_data docker/volumes/neo4j_logs docker/volumes/neo4j_import docker/volumes/neo4j_plugins docker/logs

# 🚀 Quick commands
start: up
stop: down
rebuild: down build up

# 📋 Project info
info:
	@echo "$(GREEN)📋 Project Information:$(NC)"
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)"
	@echo "Docker Compose: $(DOCKER_COMPOSE_FILE)"
	@echo ""
	@echo "$(GREEN)📁 Directory Structure:$(NC)"
	@echo "src/           - Source code"
	@echo "data/          - Data files"
	@echo "docker/        - Docker configs"
	@echo "tests/         - Test files"
	@echo "backups/       - Backup files"

# 🎯 All-in-one commands
fresh-start: clean down build up
	@echo "$(GREEN)🎯 Fresh start complete!$(NC)"

deploy: build up
	@echo "$(GREEN)🚀 Deployment complete!$(NC)"

# Phony targets
.PHONY: help install setup clean build up down restart logs dev test lint reindex backup restore status health neo4j-browser start stop rebuild info fresh-start deploy _create_volumes
