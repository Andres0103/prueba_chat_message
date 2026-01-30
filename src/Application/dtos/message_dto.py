#Importante: Este archivo define los DTOs (Data Transfer Objects) utilizados en los casos de uso relacionados con mensajes.
#Importar las librerías necesarias
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

#Dataclass para definir los DTOs relacionados con mensajes

#CreateMessageDTO representa los datos necesarios para crear un mensaje
@dataclass
class CreateMessageDTO:
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str

#MessageResponseDTO representa los datos devueltos al procesar un mensaje
@dataclass
class MessageResponseDTO:
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: Optional[Dict]

#MessageDTO es un DTO genérico para representar un mensaje en las respuestas de los casos de uso
@dataclass
class MessageDTO:
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: Optional[Dict]