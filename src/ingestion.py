import os

import nest_asyncio
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.kg.shared_storage import initialize_share_data, initialize_pipeline_status
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
        working_dir=working_dir,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
        graph_storage="Neo4JStorage",
        vector_storage="FaissVectorDBStorage",
        chunk_token_size=1500,
        chunk_overlap_token_size=300
    )

    await rag.initialize_storages()

    # ensure shared dicts exist
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

