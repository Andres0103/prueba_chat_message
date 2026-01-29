from pydantic import BaseModel
from typing import Any


class SuccessResponse(BaseModel):
    """
    Respuesta estándar para operaciones exitosas.
    """

    status: str = "success"
    data: Any
