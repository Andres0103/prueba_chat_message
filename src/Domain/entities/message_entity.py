#Definición de la entidad de dominio para mensajes, es decir, la representación central del mensaje en el sistema.
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..value_objects.sender_type import SenderType
from ..value_objects.message_metadata import MessageMetadata

#Dataclass que representa la entidad de dominio Message contiene la lógica de negocio relacionada con los mensajes
@dataclass(frozen=True)
class MessageEntity:
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: SenderType
    metadata: Optional[MessageMetadata] = None
    
    def __post_init__(self):
        #validaciones básicas del mensaje
        if not self.message_id:
            raise ValueError("message_id no puede estar vacío")
        
        if not self.session_id:
            raise ValueError("session_id no puede estar vacío")
        
        if not self.content or not self.content.strip():
            raise ValueError("content no puede estar vacío")
        
        if not isinstance(self.sender, SenderType):
            raise ValueError(f"sender debe ser de tipo 'system' o 'user', se recibió {type(self.sender)}")
    
    def with_metadata(self, metadata: MessageMetadata) -> 'MessageEntity':
        #Retorna una nueva instancia de MessageEntity con metadata actualizada
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
        #verifica si el mensaje es del usuario
        return self.sender == SenderType.USER
    
    @property
    def is_from_system(self) -> bool:
        #verifica si el mensaje es del sistema
        return self.sender == SenderType.SYSTEM