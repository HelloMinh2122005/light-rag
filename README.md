# 🚀 LightRAG - Intelligent Document Q&A System

<div align="center">

![LightRAG Logo](https://github.com/HKUDS/LightRAG/blob/main/README.assets/b2aaf634151b4706892693ffb43d9093.png?raw=true)

**Hệ thống trả lời câu hỏi thông minh dựa trên tài liệu với Knowledge Graph**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.15-green.svg)](https://neo4j.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📖 Tổng quan

LightRAG là một hệ thống **RAG (Retrieval-Augmented Generation)** hiện đại, cho phép bạn trò chuyện thông minh với tài liệu của mình. Hệ thống sử dụng **Knowledge Graph** (Neo4j) để hiểu mối quan hệ giữa các thông tin và **Vector Search** để tìm kiếm semantic chính xác.

### ✨ Tính năng chính

- 🧠 **Trí tuệ nhân tạo**: Sử dụng OpenAI GPT-4o-mini để trả lời câu hỏi
- 🕸️ **Knowledge Graph**: Neo4j lưu trữ mối quan hệ giữa các khái niệm
- 🔍 **Vector Search**: Tìm kiếm semantic với Faiss
- 🏗️ **Kiến trúc MVC**: Code được tổ chức chuẩn, dễ maintain
- 🐳 **Docker Ready**: Deploy nhanh chóng với Docker
- 📊 **Monitoring**: Health checks và logging đầy đủ
- 🔄 **Auto Indexing**: Tự động đánh chỉ mục dữ liệu mới

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   LightRAG      │
│   (Browser)     │───▶│   Controller    │───▶│   Service       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                              ┌─────────────────────────┼─────────────────────────┐
                              ▼                         ▼                         ▼
                    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
                    │     Neo4j       │    │     Faiss       │    │    OpenAI       │
                    │ Knowledge Graph │    │ Vector Search   │    │   GPT-4 Mini    │
                    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 📋 Yêu cầu hệ thống

- **Docker** và **Docker Compose** (v2.0+)
- **Make** (có sẵn trên Linux/macOS, Windows có thể dùng PowerShell)
- **OpenAI API Key**
- **Windows**: PowerShell 5.1+ (khuyến nghị) hoặc Git Bash

### ⚡ Cài đặt nhanh (5 phút)

```bash
# 1. Clone repository
git clone https://github.com/HelloMinh2122005/light-rag.git
cd light_rag

# 2. Setup dự án (tạo .env, thư mục cần thiết)
make setup

# 3. Chỉnh sửa file .env với API key của bạn
nano .env  # hoặc notepad .env trên Windows

# 4. Build và start tất cả services
make up

# 5. Kiểm tra hệ thống
make health
```

**🎉 Xong! API sẽ chạy tại http://localhost:8000**

## 🔧 Cấu hình

### 📝 File .env

Tạo file `.env` trong thư mục root với nội dung:

```env
# 🔑 OpenAI API (Bắt buộc)
OPENAI_API_KEY=sk-your-openai-api-key-here

# 🗃️ Neo4j Database
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# 📂 Application Config
DATA_PATH=/app/data/data.txt
RAG_STORAGE_PATH=/app/rag_storage
```

### 📁 Dữ liệu

Đặt file tài liệu của bạn vào thư mục `data/`:

```bash
data/
└── data.txt    # File tài liệu chính (thay bằng file của bạn)
```

## 🛠️ Lệnh Make cơ bản

### 📦 Setup & Installation

```bash
make help           # 📖 Xem tất cả lệnh có thể dùng
make setup          # 🔧 Setup dự án lần đầu
make install        # 📦 Cài đặt Python dependencies
make clean          # 🧹 Dọn dẹp cache và temp files
```

### 🐳 Docker Operations

```bash
make build          # 🔨 Build Docker images
make up             # 🚀 Start tất cả services
make down           # 🛑 Stop tất cả services  
make restart        # 🔄 Restart services
make logs           # 📝 Xem logs realtime
```

### ⚙️ Development

```bash
make dev            # 💻 Chạy development mode (local)
```

### 📊 Data Management

```bash
make reindex        # 🔄 Đánh chỉ mục lại khi có data mới
make backup         # 💾 Backup dữ liệu
make restore        # 🔄 Restore từ backup
```

### 🔍 Monitoring

```bash
make status         # 📊 Kiểm tra trạng thái services
make health         # ❤️ Health check API
make neo4j-browser  # 🗃️ Mở Neo4j Browser
```

## 📚 Hướng dẫn sử dụng

### 🎯 Workflow cơ bản

1. **Setup lần đầu:**
   ```bash
   make setup
   # Chỉnh sửa .env với API key
   make up
   ```

2. **Khi có dữ liệu mới:**
   ```bash
   # Copy file mới vào data/
   cp your-new-document.txt data/
   # Đánh chỉ mục lại
   make reindex
   ```

3. **Restart khi cần:**
   ```bash
   make restart
   ```

4. **Monitor hệ thống:**
   ```bash
   make status
   make logs
   ```

### 🌐 API Endpoints

Sau khi start thành công, bạn có thể truy cập:

| Service | URL | Mô tả |
|---------|-----|-------|
| **API Main** | http://localhost:8000 | Endpoint chính |
| **API Docs** | http://localhost:8000/docs | Swagger documentation |
| **Health Check** | http://localhost:8000/health | Kiểm tra sức khỏe |
| **Neo4j Browser** | http://localhost:7474 | Giao diện quản lý graph |
| **Reindex** | http://localhost:8000/reindex | Đánh chỉ mục lại dữ liệu |

### 📡 Sử dụng API

#### Gửi câu hỏi:

```bash
# Sử dụng curl (Linux/macOS/Git Bash)
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Napoleon là ai?",
       "mode": "hybrid",
       "top_k": 5
     }'

# Hoặc sử dụng PowerShell (Windows)
$body = @{
    question = "Napoleon là ai?"
    mode = "hybrid"
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/query" -Method Post -Body $body -ContentType "application/json"
```

#### Health Check:

```bash
# curl
curl http://localhost:8000/health

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

#### Đánh chỉ mục lại:

```bash
# curl
curl -X POST "http://localhost:8000/reindex"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/reindex" -Method Post

# Hoặc sử dụng make command
make reindex
```

### 🎨 Các chế độ tìm kiếm

- **`naive`**: Tìm kiếm vector đơn giản, nhanh nhất
- **`local`**: Tìm kiếm cục bộ, cân bằng tốc độ/chất lượng  
- **`global`**: Tìm kiếm toàn cục, chậm nhưng đầy đủ nhất
- **`mix`**: Kết hợp vector + graph, **được khuyến nghị**

## 🔧 Troubleshooting

### ❌ Lỗi thường gặp

#### 1. **"Port 8000 already in use"**
```bash
# Tìm process đang dùng port
netstat -tulpn | grep 8000  # Linux
netstat -ano | findstr 8000  # Windows

# Stop services và restart
make down
make up
```

#### 2. **"OpenAI API key not found"**
```bash
# Kiểm tra .env file
type .env  # Windows
cat .env   # Linux/macOS
# Đảm bảo có: OPENAI_API_KEY=sk-...
```

#### 3. **"Neo4j connection failed"**
```bash
# Kiểm tra Neo4j container
make status
docker logs lightrag_neo4j

# Restart Neo4j
make restart
```

#### 4. **"Docker Compose version warning"**
```bash
# Warning này đã được fix trong phiên bản mới
# Nếu vẫn gặp, cập nhật Docker Compose:
# Windows: Docker Desktop -> Update
# Linux: sudo apt update && sudo apt install docker-compose-plugin
```

### 🔍 Debug commands

```bash
# Xem logs chi tiết
make logs

# Kiểm tra containers
make status

# Test health (Windows compatible)
make health

# Vào container để debug
make shell

# Test API endpoints
make test-api
```

### 🪟 Windows Users

Dự án đã được tối ưu hóa cho Windows:
- ✅ PowerShell commands thay vì curl
- ✅ Tương thích với Docker Desktop  
- ✅ Makefile hoạt động native trên Windows
- ✅ Không cần WSL hay Git Bash

## 📁 Cấu trúc dự án

```
light_rag/
├── 📄 README.md              # Tài liệu này
├── 🛠️  Makefile              # Commands tự động
├── 📋 requirements.txt       # Python dependencies
├── ⚙️  .env                  # Cấu hình (tạo từ setup)
├── 📂 data/                  # Dữ liệu đầu vào
│   └── data.txt
├── 🐳 docker/                # Docker configs  
│   ├── Dockerfile
│   └── docker-compose.yaml
├── 💻 src/                   # Source code
│   ├── main.py              # Entry point
│   ├── ingestion.py         # Data processing
│   ├── controller/          # API controllers
│   ├── service/             # Business logic
│   ├── dto/                 # Data models
│   └── util/                # Utilities
└── 💾 backups/              # Backup files (tạo bởi make backup)
```

## 🚀 Deployment

### 🔄 Development

```bash
# Chạy local (không dùng Docker)
make dev

# Chạy với Docker (khuyến nghị)
make up
```

### 🏭 Production

```bash
# Build và deploy
make deploy

# Monitor
make status
make logs

# Backup định kỳ
make backup
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📄 License

Dự án này được phân phối dưới MIT License. Xem `LICENSE` file để biết thêm chi tiết.

## 🆘 Hỗ trợ

- 📖 **Documentation**: Đọc tài liệu trong `src/ARCHITECTURE.md`
- 🐛 **Bug Reports**: Tạo issue trên GitHub
- 💬 **Questions**: Thảo luận trong Discussions
- 📧 **Contact**: phandinhminh48@gmail.com

## 🙏 Cảm ơn

- [LightRAG](https://github.com/HKUDS/LightRAG) - Core RAG framework
- [OpenAI](https://openai.com) - GPT models
- [Neo4j](https://neo4j.com) - Graph database
- [FastAPI](https://fastapi.tiangolo.com) - Web framework

---

<div align="center">

**🎉 Happy Coding với LightRAG! 🎉**

Nếu project hữu ích, hãy cho 1 ⭐ nhé!

</div>
