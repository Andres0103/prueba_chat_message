"""
Domain Layer - Message Entity
Entidad de dominio pura sin dependencias de frameworks.
Representa un mensaje en el sistema.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..value_objects.sender_type import SenderType
from ..value_objects.message_metadata import MessageMetadata


@dataclass(frozen=True)
class MessageEntity:
    """
    Entidad de dominio que representa un mensaje.
    Es inmutable y contiene la lógica de negocio pura.
    """
    
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: SenderType
    metadata: Optional[MessageMetadata] = None
    
    def __post_init__(self):
        """Validaciones de negocio."""
        if not self.message_id:
            raise ValueError("message_id cannot be empty")
        
        if not self.session_id:
            raise ValueError("session_id cannot be empty")
        
        if not self.content or not self.content.strip():
            raise ValueError("content cannot be empty")
        
        if not isinstance(self.sender, SenderType):
            raise ValueError(f"sender must be of type SenderType, got {type(self.sender)}")
    
    def with_metadata(self, metadata: MessageMetadata) -> 'MessageEntity':
        """Retorna una nueva instancia del mensaje con metadatos."""
        return MessageEntity(
            message_id=self.message_id,
            session_id=self.session_id,
            content=self.content,
            timestamp=self.timestamp,
            sender=self.sender,
            metadata=metadata
        )
    
    @property
    def is_from_user(self) -> bool:
        """Verifica si el mensaje es de un usuario."""
        return self.sender == SenderType.USER
    
    @property
    def is_from_system(self) -> bool:
        """Verifica si el mensaje es del sistema."""
        return self.sender == SenderType.SYSTEM