from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

@dataclass
class CreateMessageDTO:
    """
    DTO de entrada para crear un mensaje.
    Representa los datos necesarios para el caso de uso.
    """

    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str

@dataclass
class MessageResponseDTO:
    """
    DTO de salida para respuestas de mensajes procesados.
    """

    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: Optional[Dict]