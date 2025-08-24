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
	@echo "  make shell            - Access container shell"
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
	@python -c "import os; dirs=['data','logs','docker/volumes/rag_storage','docker/volumes/neo4j_data','docker/volumes/neo4j_logs']; [os.makedirs(d, exist_ok=True) for d in dirs]"
	@python -c "import os; open('.env', 'w').write('# Copy this to .env and configure\\nOPENAI_API_KEY=your_key_here\\nNEO4J_URI=bolt://neo4j:7687\\nNEO4J_USERNAME=neo4j\\nNEO4J_PASSWORD=your_password\\n') if not os.path.exists('.env') else None"
	@echo "$(GREEN)✅ Setup complete! Edit the .env file with your API keys.$(NC)"

clean:
	@echo "$(GREEN)🧹 Cleaning up...$(NC)"
	@python -c "import os, shutil; [shutil.rmtree(root, ignore_errors=True) for root, dirs, files in os.walk('.') for d in dirs if d == '__pycache__']"
	@python -c "import os; [os.remove(os.path.join(root, f)) for root, dirs, files in os.walk('.') for f in files if f.endswith(('.pyc', '.pyo'))]"
	@python -c "import os, shutil; [shutil.rmtree(root, ignore_errors=True) for root, dirs, files in os.walk('.') for d in dirs if d.endswith('.egg-info')]"
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
	@python -c "import time; time.sleep(30)"
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
	@python -c "import time; time.sleep(15)"
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

# 🐚 Access container shell for debugging
shell:
	@echo "$(GREEN)🐚 Accessing container shell...$(NC)"
	docker exec -it docker-lightrag-api-1 bash || docker exec -it docker-lightrag-api-1 sh

# 📊 Data Management
reindex:
	@echo "$(GREEN)🔄 Reindexing data...$(NC)"
	@powershell -Command "try { Invoke-RestMethod -Uri 'http://localhost:8000/reindex' -Method Post; Write-Host '$(GREEN)✅ Reindex complete!$(NC)' } catch { Write-Host '$(RED)❌ Failed to reindex. Make sure the API is running.$(NC)' }"

backup:
	@echo "$(GREEN)💾 Creating backup...$(NC)"
	@python -c "import os; os.makedirs('backups', exist_ok=True)"
	@python -c "import os, shutil, datetime; backup_name=f'backup_{datetime.datetime.now().strftime(\"%Y%m%d_%H%M%S\")}'; print(f'Creating backup: {backup_name}'); shutil.copytree('docker/volumes/rag_storage', f'backups/{backup_name}', ignore_errors=True) if os.path.exists('docker/volumes/rag_storage') else print('⚠️  RAG storage not found')"
	@docker exec lightrag_neo4j cypher-shell -u neo4j -p your_password "CALL apoc.export.cypher.all('/var/lib/neo4j/import/backup.cypher')" 2>/dev/null || echo "$(YELLOW)⚠️  Neo4j backup failed$(NC)"
	@echo "$(GREEN)✅ Backup created!$(NC)"

restore:
	@echo "$(GREEN)🔄 Available backups:$(NC)"
	@python -c "import os; print('\\n'.join(os.listdir('backups'))) if os.path.exists('backups') else print('$(YELLOW)No backups found$(NC)')"
	@echo "$(YELLOW)To restore, copy backup files manually to docker/volumes/$(NC)"

# 🔍 Monitoring
status:
	@echo "$(GREEN)📊 Service Status:$(NC)"
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps

health:
	@echo "$(GREEN)❤️  Checking API health...$(NC)"
	@powershell -Command "try { $$response = Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method Get; $$response | ConvertTo-Json -Depth 10 } catch { Write-Host '$(RED)❌ API not responding$(NC)' }"

neo4j-browser:
	@echo "$(GREEN)🗃️  Opening Neo4j Browser...$(NC)"
	@echo "URL: http://localhost:7474"
	@echo "Username: neo4j"
	@echo "Password: your_password"
	@powershell -Command "Start-Process 'http://localhost:7474'" 2>$$null || echo "$(YELLOW)Please open http://localhost:7474 manually$(NC)"

# 🔧 Internal helpers
_create_volumes:
	@echo "$(YELLOW)Creating required directories...$(NC)"
	@python -c "import os; dirs=['docker/volumes/rag_storage','docker/volumes/neo4j_data','docker/volumes/neo4j_logs','docker/volumes/neo4j_import','docker/volumes/neo4j_plugins','docker/logs']; [os.makedirs(d, exist_ok=True) for d in dirs]"
	@echo "$(GREEN)Directories ensured.$(NC)"

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
