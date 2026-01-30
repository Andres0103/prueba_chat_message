from pydantic import BaseModel
from typing import Any


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Any


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: str
    error: str | None = None
