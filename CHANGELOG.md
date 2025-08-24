# 📝 Changelog

Tất cả các thay đổi quan trọng của dự án sẽ được ghi lại ở đây.

## [1.0.0] - 2025-08-24

### 🎉 Initial Release

#### ✨ Added
- **Core RAG System**: Hệ thống RAG hoàn chỉnh với LightRAG
- **Knowledge Graph**: Tích hợp Neo4j để lưu trữ mối quan hệ
- **Vector Search**: Sử dụng Faiss cho tìm kiếm semantic
- **OpenAI Integration**: GPT-4 Mini cho generation
- **MVC Architecture**: Tách biệt Controller, Service, Utility layers
- **Docker Support**: Containerization hoàn chỉnh
- **Health Monitoring**: Health checks và logging
- **API Documentation**: Swagger/OpenAPI docs

#### 🏗️ Architecture
- **Controller Layer**: `controller/rag_controller.py` - HTTP request handling
- **Service Layer**: `service/rag_service.py` - Business logic
- **Utility Layer**: `util/text_search_util.py` - Helper functions
- **DTO Layer**: `dto/` - Data transfer objects

#### 🐳 Docker & DevOps
- **Multi-service**: LightRAG API + Neo4j + volumes
- **Persistent Storage**: Data persistence cho RAG indexes và Neo4j
- **Auto-dependency**: Dependency management giữa services
- **Health Checks**: Container health monitoring

#### 🛠️ Development Tools
- **Makefile**: 20+ commands để quản lý dự án
- **Scripts**: Automated setup và deployment
- **Testing**: API test script
- **Documentation**: Comprehensive README và architecture docs

#### 📊 Features
- **Multiple Search Modes**: naive, local, global, hybrid
- **Auto Indexing**: Tự động đánh chỉ mục dữ liệu
- **Fallback Mechanism**: Text search fallback khi RAG fail
- **Real-time Logs**: Live logging và monitoring
- **Backup/Restore**: Data backup utilities

### 🔧 Configuration
- **Environment Variables**: Comprehensive .env configuration
- **Flexible Paths**: Configurable data và storage paths
- **Performance Tuning**: Adjustable chunk sizes và parameters

### 📚 Documentation
- **README**: Complete setup và usage guide
- **Architecture Doc**: Detailed system architecture
- **API Docs**: Auto-generated Swagger documentation
- **Docker Docs**: Container setup và management

---

## 🚀 Future Plans

### [1.1.0] - Planned
- [ ] **Authentication**: User authentication và authorization
- [ ] **Multi-tenant**: Support multiple users/tenants
- [ ] **File Upload**: Web interface để upload documents
- [ ] **Batch Processing**: Xử lý nhiều documents cùng lúc
- [ ] **Metrics**: Prometheus metrics integration

### [1.2.0] - Planned  
- [ ] **Web UI**: React/Vue frontend
- [ ] **Chat Interface**: Conversational AI interface
- [ ] **Document Management**: CRUD operations cho documents
- [ ] **Advanced Search**: Complex query capabilities
- [ ] **Caching**: Redis caching layer

### [2.0.0] - Planned
- [ ] **Microservices**: Break down into microservices
- [ ] **Kubernetes**: K8s deployment configs
- [ ] **Multi-language**: Support for multiple languages
- [ ] **Plugin System**: Extensible plugin architecture
- [ ] **Enterprise Features**: Advanced enterprise capabilities

---

## 📋 Migration Guide

### From Manual Setup to Docker
If you were running components manually:

1. **Stop manual services**:
   ```bash
   # Stop any running Neo4j
   docker stop neo4j && docker rm neo4j
   ```

2. **Backup data** (if needed):
   ```bash
   make backup
   ```

3. **Start with Docker**:
   ```bash
   make up
   ```

### Configuration Changes
- **Neo4j URI**: Change from `bolt://localhost:7687` to `bolt://neo4j:7687` trong Docker
- **Paths**: Use container paths (`/app/data/`) thay vì local paths
- **Environment**: All config trong `.env` file

---

## 🐛 Known Issues

### [1.0.0]
- **Memory Usage**: High memory usage với large documents
- **Cold Start**: Slow startup time khi initialize RAG
- **Error Handling**: Cần improve error messages

### Workarounds
- **Memory**: Giảm `chunk_token_size` trong config
- **Startup**: Tăng `start_period` trong health checks
- **Errors**: Check logs với `make logs`

---

## 🤝 Contributing

Xem [CONTRIBUTING.md](CONTRIBUTING.md) để biết cách contribute.

---

## 📄 License

MIT License - xem [LICENSE](LICENSE) file.
