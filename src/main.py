# Import các thư viện cần thiết
from fastapi import FastAPI        # Tạo web API
import uvicorn                     # Máy chủ web để chạy API
from controller.rag_controller import RAGController
from dto.QueryRequest import QueryRequest
from dto.QueryResponse import QueryResponse

# Khởi tạo ứng dụng FastAPI (tạo website API)
app = FastAPI(
    title="LightRAG API",                         # Tên ứng dụng
    description="API for querying RAG system",    # Mô tả chức năng
    version="1.0.0"                              # Phiên bản
)

# Khởi tạo controller
rag_controller = RAGController()

@app.on_event("startup")
async def startup_event():
    """
    Khởi tạo hệ thống RAG khi ứng dụng bắt đầu chạy
    """
    await rag_controller.initialize_system()

@app.get("/")
async def root():
    """
    Endpoint kiểm tra sức khỏe cơ bản - trang chủ
    """
    return rag_controller.get_basic_info()

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Endpoint chính để hỏi đáp với hệ thống RAG
    Đây là nơi người dùng gửi câu hỏi và nhận câu trả lời
    
    Args:
        request: QueryRequest chứa câu hỏi và các tham số
        
    Returns:
        QueryResponse với câu trả lời
    """
    return await rag_controller.process_query(request)

@app.get("/health")
async def health_check():
    """
    Endpoint kiểm tra sức khỏe chi tiết của hệ thống
    """
    return await rag_controller.get_health_status()

@app.post("/reindex")
async def reindex_data():
    """
    Buộc đánh chỉ mục lại dữ liệu
    Dùng khi muốn cập nhật dữ liệu mới
    """
    return await rag_controller.reindex_data()

if __name__ == "__main__":
    # Chạy máy chủ web
    print("Starting LightRAG HTTP Server...")
    uvicorn.run(
        "main:app",                           # Tên module:ứng dụng
        host="0.0.0.0",                       # Lắng nghe tất cả địa chỉ IP
        port=8000,                            # Cổng 8000
        reload=False,                         # Không tự động reload
        log_level="info"                      # Mức độ log
    )
