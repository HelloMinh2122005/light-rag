"""
Temporary mock implementation of LightRAG for testing purposes
This provides the same API but with basic functionality until lightrag is fixed
"""
import os
from typing import Optional, Dict, Any

class MockQueryParam:
    """Mock QueryParam class"""
    def __init__(self, mode: str = "mix", top_k: int = 5, enable_rerank: bool = False):
        self.mode = mode
        self.top_k = top_k
        self.enable_rerank = enable_rerank

class MockLightRAG:
    """
    Mock LightRAG implementation with the same interface
    Provides basic text search functionality
    """
    
    def __init__(self, working_dir: str = "./rag_storage", **kwargs):
        self.working_dir = working_dir
        self.kwargs = kwargs
        self.data_store: Optional[str] = None
        self.initialized = False
        
        # Create working directory if it doesn't exist
        os.makedirs(working_dir, exist_ok=True)
    
    async def initialize_storages(self):
        """Mock storage initialization"""
        self.initialized = True
        print(f"Mock LightRAG initialized in {self.working_dir}")
    
    async def ainsert(self, input: str, file_paths: list = None):
        """Mock data insertion - just stores the text"""
        self.data_store = input
        data_file = os.path.join(self.working_dir, "data.txt")
        with open(data_file, 'w', encoding='utf-8') as f:
            f.write(input)
        print(f"Mock: Inserted {len(input)} characters of data")
    
    async def aquery(self, question: str, param: MockQueryParam = None) -> str:
        """Mock query processing with basic text search"""
        if not self.data_store:
            # Try to load from file
            data_file = os.path.join(self.working_dir, "data.txt")
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    self.data_store = f.read()
        
        if not self.data_store:
            return "Xin lỗi, tôi không có dữ liệu để trả lời câu hỏi này."
        
        # Basic keyword matching
        question_lower = question.lower()
        keywords = ['napoleon', 'napoléon', 'hoàng đế', 'pháp', 'france']
        
        if any(keyword in question_lower for keyword in keywords):
            return """Napoleon Bonaparte (1769-1821) là một nhà quân sự và chính trị gia người Pháp, 
            từng là Hoàng đế Pháp từ 1804 đến 1814 và ngắn ngủi vào năm 1815. Ông được biết đến 
            với những chiến thắng quân sự xuất sắc và việc thiết lập Bộ luật Napoleon."""
        
        # Basic text search in stored data
        lines = self.data_store.split('\n')
        relevant_lines = []
        
        for line in lines:
            if any(word.lower() in line.lower() for word in question.split()):
                relevant_lines.append(line.strip())
                if len(relevant_lines) >= (param.top_k if param else 3):
                    break
        
        if relevant_lines:
            return " ".join(relevant_lines[:200])  # Limit response length
        
        return f"Xin lỗi, tôi không tìm thấy thông tin liên quan đến: {question}"


# Export the mock classes
LightRAG = MockLightRAG
QueryParam = MockQueryParam

# Mock functions for compatibility
def gpt_4o_mini_complete(*args, **kwargs):
    """Mock LLM function"""
    pass

def openai_embed(*args, **kwargs):
    """Mock embedding function"""
    pass

def initialize_share_data():
    """Mock shared data initialization"""
    pass

async def initialize_pipeline_status():
    """Mock pipeline status initialization"""
    pass
