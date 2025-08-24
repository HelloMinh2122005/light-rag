"""
Utility Layer - Các hàm tiện ích và xử lý phụ trợ
Chứa logic tìm kiếm văn bản dự phòng và các tiện ích khác
"""

import re
from typing import List, Tuple


class TextSearchUtil:
    """
    Lớp tiện ích để xử lý tìm kiếm văn bản đơn giản
    Dùng làm dự phòng khi hệ thống RAG chính gặp lỗi
    """

    @staticmethod
    def local_search(text: str, question: str, top_k: int = 5) -> str:
        """
        Tìm kiếm dự phòng rất đơn giản: đánh giá đoạn văn bằng cách 
        đếm số từ trùng lặp với câu hỏi.
        
        Args:
            text: Văn bản gốc để tìm kiếm
            question: Câu hỏi của người dùng
            top_k: Số đoạn văn tối đa trả về
            
        Returns:
            Chuỗi văn bản kết quả từ các đoạn văn phù hợp nhất
        """
        if not text or not question:
            return "Sorry, I'm not able to provide an answer to that question.[no-input]"

        # Chia thành các đoạn văn bằng dòng trống
        paragraphs = TextSearchUtil._split_into_paragraphs(text)
        
        # Tính điểm cho từng đoạn văn
        scored_paragraphs = TextSearchUtil._score_paragraphs(paragraphs, question)
        
        # Lấy các đoạn văn tốt nhất
        top_paragraphs = TextSearchUtil._get_top_paragraphs(scored_paragraphs, top_k)
        
        if not top_paragraphs:
            return "Sorry, I'm not able to provide an answer to that question.[no-context]"
        
        return "\n\n".join(top_paragraphs)

    @staticmethod
    def _split_into_paragraphs(text: str) -> List[str]:
        """
        Chia văn bản thành các đoạn văn
        
        Args:
            text: Văn bản gốc
            
        Returns:
            Danh sách các đoạn văn
        """
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        return paragraphs

    @staticmethod
    def _extract_tokens(text: str) -> set:
        """
        Trích xuất các từ từ văn bản
        
        Args:
            text: Văn bản đầu vào
            
        Returns:
            Tập hợp các từ đã được chuẩn hóa
        """
        return set(re.findall(r"\w+", text.lower()))

    @staticmethod
    def _score_paragraphs(paragraphs: List[str], question: str) -> List[Tuple[int, str]]:
        """
        Tính điểm cho từng đoạn văn dựa trên độ tương đồng với câu hỏi
        
        Args:
            paragraphs: Danh sách các đoạn văn
            question: Câu hỏi
            
        Returns:
            Danh sách tuple (điểm, đoạn_văn) đã sắp xếp
        """
        question_tokens = TextSearchUtil._extract_tokens(question)
        scores = []
        
        for paragraph in paragraphs:
            paragraph_tokens = TextSearchUtil._extract_tokens(paragraph)
            overlap = len(question_tokens & paragraph_tokens)  # Số từ trùng lặp
            scores.append((overlap, paragraph))
        
        # Sắp xếp theo điểm từ cao đến thấp
        scores.sort(reverse=True, key=lambda x: x[0])
        return scores

    @staticmethod
    def _get_top_paragraphs(scored_paragraphs: List[Tuple[int, str]], top_k: int) -> List[str]:
        """
        Lấy các đoạn văn có điểm cao nhất
        
        Args:
            scored_paragraphs: Danh sách (điểm, đoạn_văn) đã sắp xếp
            top_k: Số đoạn văn tối đa
            
        Returns:
            Danh sách các đoạn văn tốt nhất
        """
        top_paragraphs = [paragraph for score, paragraph in scored_paragraphs[:top_k] if score > 0]
        return top_paragraphs


class ValidationUtil:
    """
    Lớp tiện ích để validate dữ liệu đầu vào
    """

    @staticmethod
    def validate_file_path(file_path: str) -> Tuple[bool, str]:
        """
        Kiểm tra tính hợp lệ của đường dẫn file
        
        Args:
            file_path: Đường dẫn file cần kiểm tra
            
        Returns:
            Tuple (is_valid, error_message)
        """
        import os
        
        if not file_path:
            return False, "File path is empty"
        
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        
        if not os.path.isfile(file_path):
            return False, f"Path is not a file: {file_path}"
        
        if os.path.getsize(file_path) == 0:
            return False, f"File is empty: {file_path}"
        
        return True, ""

    @staticmethod
    def validate_query_params(question: str, mode: str, top_k: int) -> Tuple[bool, str]:
        """
        Kiểm tra tính hợp lệ của tham số truy vấn
        
        Args:
            question: Câu hỏi
            mode: Chế độ tìm kiếm
            top_k: Số kết quả tối đa
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not question or not question.strip():
            return False, "Question cannot be empty"
        
        valid_modes = ["naive", "local", "global", "hybrid", "mix"]
        if mode not in valid_modes:
            return False, f"Invalid mode. Must be one of: {valid_modes}"
        
        if not isinstance(top_k, int) or top_k < 1 or top_k > 50:
            return False, "top_k must be an integer between 1 and 50"
        
        return True, ""


class LogUtil:
    """
    Lớp tiện ích để ghi log có cấu trúc
    """

    @staticmethod
    def log_info(message: str, component: str = "RAG"):
        """
        Ghi log thông tin
        """
        print(f"[INFO] [{component}] {message}")

    @staticmethod
    def log_error(message: str, component: str = "RAG", exception: Exception = None):
        """
        Ghi log lỗi
        """
        error_msg = f"[ERROR] [{component}] {message}"
        if exception:
            error_msg += f" - Exception: {str(exception)}"
        print(error_msg)

    @staticmethod
    def log_warning(message: str, component: str = "RAG"):
        """
        Ghi log cảnh báo
        """
        print(f"[WARNING] [{component}] {message}")
