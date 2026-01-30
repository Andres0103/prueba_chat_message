#Importante: Este archivo define los DTOs (Data Transfer Objects) utilizados para la paginación y filtros de mensajes.
#Importar las librerías necesarias
from typing import List, TypeVar, Generic, Optional
from pydantic import BaseModel, Field


T = TypeVar("T") # Tipo genérico para los elementos paginados

#PaginationDTO es un DTO genérico para respuestas paginadas
class PaginationDTO(BaseModel, Generic[T]):
    items: List[T]
    limit: int = Field(..., description="Número máximo de elementos por página")
    offset: int = Field(..., description="Número de elementos a saltar")
    total: int = Field(..., description="Número total de elementos")

    class Config:
        arbitrary_types_allowed = True

#GetMessagesFilterDTO es un DTO específico para los filtros de consulta de mensajes
class GetMessagesFilterDTO(BaseModel):
    session_id: str = Field(..., description="ID de la sesión")
    limit: int = Field(default=20, ge=1, le=100, description="Límite de mensajes por página")
    offset: int = Field(default=0, ge=0, description="Desplazamiento para paginación")
    sender: Optional[str] = Field(default=None, description="Filtro opcional por remitente")
