"""
Domain Layer - Message Metadata Value Object
Objeto de valor inmutable que contiene metadatos del mensaje.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MessageMetadata:
    """Metadatos procesados de un mensaje."""
    
    word_count: int
    character_count: int
    processed_at: datetime
    
    @classmethod
    def from_content(cls, content: str) -> 'MessageMetadata':
        """Crea metadatos a partir del contenido del mensaje."""
        return cls(
            word_count=len(content.split()),
            character_count=len(content),
            processed_at=datetime.utcnow()
        )
    
    def to_dict(self) -> dict:
        return {
            "word_count": self.word_count,
            "character_count": self.character_count,
            "processed_at": self.processed_at.isoformat()
        }