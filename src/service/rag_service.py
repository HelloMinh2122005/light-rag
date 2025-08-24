"""
Service Layer - Xử lý logic nghiệp vụ chính của hệ thống RAG
Chứa tất cả logic xử lý RAG, khởi tạo và tìm kiếm
"""

import os
from typing import Optional
from lightrag import LightRAG, QueryParam
from ingestion import initialize_rag, index_file
from util.text_search_util import TextSearchUtil


class RAGService:
    """
    Lớp dịch vụ để quản lý các hoạt động của hệ thống RAG
    Đây là "bộ não" chính xử lý tất cả logic nghiệp vụ
    """
    
    def __init__(self, data_path: str = "../../data/data.txt"):
        self.data_path = data_path           # Đường dẫn đến file dữ liệu
        self.rag = None                      # Đối tượng RAG (ban đầu chưa có)
        self.raw_text: Optional[str] = None  # Văn bản dự phòng nếu RAG lỗi
        self.indexing_complete: bool = False # Trạng thái đánh chỉ mục

    async def initialize(self, force_reindex: bool = False):
        """
        Khởi tạo và đánh chỉ mục dữ liệu không đồng bộ. 
        Sử dụng hàm index_file với thử lại nhiều lần,
        và dự phòng lưu văn bản thô nếu đánh chỉ mục thất bại.
        """
        # Bước 1: Kiểm tra file dữ liệu có tồn tại không
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        # Bước 2: Kiểm tra file có rỗng không
        if os.path.getsize(self.data_path) == 0:
            raise ValueError(f"Data file is empty: {self.data_path}")

        # Bước 3: Khởi tạo RAG nếu chưa có hoặc bắt buộc tạo lại
        if self.rag is None or force_reindex:
            print("Initializing RAG system...")
            # Thử khởi tạo hệ thống RAG
            try:
                self.rag = await initialize_rag()
            except Exception as e:
                print(f"initialize_rag failed: {e}")
                # Giữ self.rag = None và tiếp tục chuẩn bị dự phòng
                self.rag = None

            print(f"Indexing data from {self.data_path}...")
            # Thử đánh chỉ mục qua index_file với nhiều lần thử
            if self.rag is not None:
                last_exc = None
                # Thử 3 lần
                for attempt in range(1, 4):
                    try:
                        print(f"index_file attempt {attempt}...")
                        await index_file(self.rag, self.data_path)
                        print("Indexing complete!")
                        last_exc = None
                        break
                    except Exception as e:
                        print(f"index_file attempt {attempt} failed: {e}")
                        last_exc = e

                # Nếu tất cả lần thử đều thất bại
                if last_exc:
                    print(f"index_file failed after retries: {last_exc}")
                    # Chuẩn bị văn bản dự phòng
                    self._prepare_fallback_text()

                    # Thử chèn trực tiếp một lần nữa nếu có thể
                    try:
                        if self.rag is not None:
                            await self.rag.ainsert(self.raw_text or "")
                            print("Fallback raw indexing complete!")
                            self.indexing_complete = True
                    except Exception as e2:
                        print(f"Fallback ainsert also failed: {e2}. Will use local text search fallback.")
                        self.indexing_complete = False
            else:
                # Không thể khởi tạo RAG; tải văn bản thô để tìm kiếm cục bộ
                self._prepare_fallback_text()
                print("Loaded raw text for local fallback search.")
                self.indexing_complete = False

        # Đánh dấu hoàn thành đánh chỉ mục nếu rag tồn tại và không có lỗi
        if self.rag is not None and self.indexing_complete is False:
            # Nếu rag tồn tại và chưa đặt indexing_complete, đặt True
            self.indexing_complete = True
        return self.rag

    def _prepare_fallback_text(self):
        """
        Chuẩn bị văn bản dự phòng để tìm kiếm cục bộ
        """
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.raw_text = content
        except Exception as e:
            print(f"Failed to load raw text for fallback: {e}")

    async def get_answer(self, question: str, mode: str = "mix", top_k: int = 5, force_reindex: bool = False) -> str:
        """
        Xử lý câu hỏi và trả về câu trả lời
        Đây là hàm chính để trả lời câu hỏi của người dùng
        """
        # Bước 1: Thử khởi tạo RAG (có thể đặt self.raw_text nếu dùng dự phòng)
        try:
            await self.initialize(force_reindex=force_reindex)
        except Exception as e:
            print(f"RAG initialization failed in get_answer: {e}")

        # Bước 2: Nếu RAG có sẵn, thử sử dụng nó
        if self.rag is not None:
            query_param = QueryParam(
                mode=mode,              # Chế độ tìm kiếm
                top_k=top_k,           # Số kết quả tối đa
                enable_rerank=False    # Không sắp xếp lại kết quả
            )
            try:
                return await self.rag.aquery(question, param=query_param)
            except Exception as e:
                print(f"RAG query failed: {e}")

        # Bước 3: Dự phòng: tìm kiếm cục bộ trên văn bản thô
        print("Using local fallback search...")
        if not self.raw_text:
            self._prepare_fallback_text()
            if not self.raw_text:
                return "Sorry, I'm not able to provide an answer to that question.[no-data]"

        # Sử dụng utility class để tìm kiếm
        text_search = TextSearchUtil()
        return text_search.local_search(self.raw_text, question, top_k)

    def get_status(self) -> dict:
        """
        Lấy trạng thái hiện tại của hệ thống RAG
        """
        return {
            "rag_initialized": self.rag is not None,
            "indexing_complete": self.indexing_complete,
            "data_path": self.data_path,
            "has_fallback_text": self.raw_text is not None
        }
