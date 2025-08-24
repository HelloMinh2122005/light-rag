"""
Controller Layer - Xử lý HTTP requests và responses
Chứa các endpoint API và logic điều khiển luồng xử lý
"""

import os
from fastapi import HTTPException
from service.rag_service import RAGService
from dto.QueryRequest import QueryRequest
from dto.QueryResponse import QueryResponse
from util.text_search_util import ValidationUtil, LogUtil


class RAGController:
    """
    Controller xử lý các yêu cầu HTTP cho hệ thống RAG
    Tách biệt logic điều khiển với logic nghiệp vụ
    """
    
    def __init__(self, data_path: str = None):
        # Use environment variable or default path that works in Docker
        if data_path is None:
            data_path = os.getenv("DATA_PATH", "/app/data/data.txt")
        self.rag_service = RAGService(data_path)
        LogUtil.log_info("RAG Controller initialized", "CONTROLLER")

    async def initialize_system(self):
        """
        Khởi tạo hệ thống RAG khi ứng dụng bắt đầu
        """
        try:
            await self.rag_service.initialize()
            LogUtil.log_info("RAG system initialized successfully", "CONTROLLER")
        except Exception as e:
            LogUtil.log_error("Failed to initialize RAG system", "CONTROLLER", e)
            raise

    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Xử lý yêu cầu truy vấn từ người dùng
        
        Args:
            request: Yêu cầu truy vấn chứa câu hỏi và tham số
            
        Returns:
            QueryResponse: Phản hồi chứa câu trả lời
            
        Raises:
            HTTPException: Nếu có lỗi trong quá trình xử lý
        """
        try:
            # Bước 1: Validate đầu vào
            is_valid, error_msg = ValidationUtil.validate_query_params(
                request.question, request.mode, request.top_k
            )
            if not is_valid:
                LogUtil.log_warning(f"Invalid query parameters: {error_msg}", "CONTROLLER")
                raise HTTPException(status_code=400, detail=error_msg)

            # Bước 2: Log thông tin truy vấn
            LogUtil.log_info(f"Processing query: {request.question[:50]}...", "CONTROLLER")
            
            # Bước 3: Gọi service để xử lý
            answer = await self.rag_service.get_answer(
                question=request.question,
                mode=request.mode,
                top_k=request.top_k,
                force_reindex=request.force_reindex
            )
            
            # Bước 4: Tạo phản hồi
            response = QueryResponse(
                question=request.question,
                answer=answer,
                mode=request.mode,
                top_k=request.top_k,
                status="success"
            )
            
            LogUtil.log_info("Query processed successfully", "CONTROLLER")
            return response
            
        except HTTPException:
            # Re-raise HTTP exceptions (validation errors)
            raise
        except Exception as e:
            # Log và chuyển đổi các exception khác thành HTTP 500
            LogUtil.log_error("Error processing query", "CONTROLLER", e)
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    async def get_health_status(self) -> dict:
        """
        Lấy trạng thái sức khỏe của hệ thống
        
        Returns:
            dict: Thông tin trạng thái hệ thống
        """
        try:
            service_status = self.rag_service.get_status()
            return {
                "status": "healthy",
                **service_status
            }
        except Exception as e:
            LogUtil.log_error("Error getting health status", "CONTROLLER", e)
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    async def reindex_data(self) -> dict:
        """
        Buộc đánh chỉ mục lại dữ liệu
        
        Returns:
            dict: Kết quả của quá trình đánh chỉ mục
            
        Raises:
            HTTPException: Nếu có lỗi trong quá trình đánh chỉ mục
        """
        try:
            LogUtil.log_info("Starting data reindexing", "CONTROLLER")
            await self.rag_service.initialize(force_reindex=True)
            LogUtil.log_info("Data reindexing completed successfully", "CONTROLLER")
            return {
                "message": "Data reindexed successfully", 
                "status": "success"
            }
        except Exception as e:
            LogUtil.log_error("Error reindexing data", "CONTROLLER", e)
            raise HTTPException(
                status_code=500,
                detail=f"Error reindexing data: {str(e)}"
            )

    def get_basic_info(self) -> dict:
        """
        Lấy thông tin cơ bản của API
        
        Returns:
            dict: Thông tin cơ bản
        """
        return {
            "message": "LightRAG API is running", 
            "status": "healthy",
            "version": "1.0.0"
        }
