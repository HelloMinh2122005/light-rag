import os

import nest_asyncio
from dotenv import load_dotenv

from lightrag import LightRAG, QueryParam

# cho phép chạy vòng lặp lồng nhau (trong Jupyter hoặc môi trường đã có vòng lặp)
nest_asyncio.apply()

# Load các biến môi trường
load_dotenv()

# Hàm khởi tạo LightRAG
async def initialize_rag(working_dir: str = "./rag_storage") -> LightRAG:
    # Bước 1: Khởi tạo LightRAG với cấu hình cơ bản
    rag = LightRAG(
        working_dir=working_dir,           # Thư mục lưu dữ liệu
        # For lightrag-hku, we'll use default OpenAI functions
        llm_model_name="gpt-4o-mini",      # Tên model ChatGPT
        embedding_model_name="text-embedding-3-large", # Model embedding
        chunk_token_size=1500,             # Chia văn bản thành đoạn 1500 từ
        chunk_overlap_token_size=300       # Chồng lấn 300 từ giữa các đoạn
    )

    # Bước 2: Khởi tạo các kho lưu trữ (nếu cần)
    # await rag.initialize_storages()

    return rag

#  Hàm đánh chỉ mục dữ liệu
async def index_data(rag: LightRAG, file_path: str) -> None:
    # Bước 1: Kiểm tra file có tồn tại không
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    # Bước 2: Đọc nội dung file
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Bước 3: Truyền các đoạn văn bản vào kho vector và đồ thị của LightRAG
    await rag.ainsert(input=text, file_paths=[file_path])


# Hàm phụ trợ
async def index_file(rag: LightRAG, path: str) -> None:
    """
    Đây chỉ là tên gọi khác của index_data() để code nhất quán
    """
    await index_data(rag, path)

