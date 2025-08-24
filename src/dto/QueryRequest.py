from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    question: str
    mode: Optional[str] = "mix"
    top_k: Optional[int] = 5
    force_reindex: Optional[bool] = False