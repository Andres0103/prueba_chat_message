from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict


class MessageCreateSchema(BaseModel):
    """
    Schema de entrada para crear un mensaje.
    """

    message_id: str = Field(..., example="msg-123456")
    session_id: str = Field(..., example="session-abcdef")
    content: str = Field(..., example="Hola, ¿cómo puedo ayudarte hoy?")
    timestamp: datetime = Field(..., example="2023-06-15T14:30:00Z")
    sender: str = Field(..., example="user")


class MessageResponseSchema(BaseModel):
    """
    Schema de salida para un mensaje procesado.
    """

    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: Optional[Dict]
