from pydantic import BaseModel
from typing import Optional


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[str] = None


class ErrorResponse(BaseModel):
    status: str = "error"
    error: ErrorDetail
