from pydantic import BaseModel
from typing import Any


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Any
