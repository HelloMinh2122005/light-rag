from pydantic import BaseModel

class QueryResponse(BaseModel):
    question: str
    answer: str
    mode: str
    top_k: int
    status: str