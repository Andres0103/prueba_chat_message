from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, List

#En este schema, se agrega message_id y session_id como campos obligatorios para la creación de mensajes Definidos por el usuario.Solo para el ejemplo de carga del mensaje. Pero no debe ser así ya que estos campos se llenan de forma automática en el backend.
#Para la respuesta del mensaje, se incluye un campo metadata opcional para información adicional. Además, se define un esquema para la paginación de mensajes.
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
