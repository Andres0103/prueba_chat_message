from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class MessageCreateSchema(BaseModel):
    message_id: str = Field(..., example="msg-123456")
    session_id: str = Field(..., example="session-abcdef")
    content: str = Field(..., example="Hola, ¿cómo puedo ayudarte hoy?")
    timestamp: datetime = Field(..., example="2023-06-15T14:30:00Z")
    sender: str = Field(..., example="user")


class MessageResponseSchema(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: Optional[Dict]


class PaginatedMessagesSchema(BaseModel):
    items: List[MessageResponseSchema] = Field(..., description="Lista de mensajes")
    limit: int = Field(..., description="Límite de mensajes por página")
    offset: int = Field(..., description="Desplazamiento en la paginación")
    total: int = Field(..., description="Número total de mensajes en la sesión")
