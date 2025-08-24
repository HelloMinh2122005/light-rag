import os

import nest_asyncio
from dotenv import load_dotenv

from lightrag import LightRAG
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.kg.shared_storage import initialize_share_data, initialize_pipeline_status

# cho phép chạy vòng lặp lồng nhau (trong Jupyter hoặc môi trường đã có vòng lặp)
nest_asyncio.apply()

# Load các biến môi trường
load_dotenv()

# Hàm khởi tạo LightRAG
async def initialize_rag(working_dir: str = "./rag_storage") -> LightRAG:
    # Bước 1: Khởi tạo LightRAG
    rag = LightRAG(
        working_dir=working_dir,           # Thư mục lưu dữ liệu
        embedding_func=openai_embed,       # Hàm chuyển text thành số
        llm_model_func=gpt_4o_mini_complete, # Hàm gọi ChatGPT
        graph_storage="Neo4JStorage",      # Lưu mối quan hệ trong Neo4j
        vector_storage="FaissVectorDBStorage", # Lưu vector trong Faiss
        chunk_token_size=1500,             # Chia văn bản thành đoạn 1500 từ
        chunk_overlap_token_size=300       # Chồng lấn 300 từ giữa các đoạn
    )

    # Bước 2: Khởi tạo các kho lưu trữ
    await rag.initialize_storages()

    # Bước 3: Chuẩn bị dữ liệu dùng chung
    # Tránh lỗi khi nhiều process cùng chạy
    initialize_share_data()
    await initialize_pipeline_status()

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

