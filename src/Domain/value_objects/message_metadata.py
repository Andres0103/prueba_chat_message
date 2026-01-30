#Contiene la definición de un objeto de valor para los metadatos del mensaje
from dataclasses import dataclass
from datetime import datetime

#Metadatos procesados de un mensaje
@dataclass(frozen=True)
class MessageMetadata:
   
    word_count: int
    character_count: int
    processed_at: datetime
    
    #crea metadatos a partir del contenido del mensaje
    @classmethod
    def from_content(cls, content: str) -> 'MessageMetadata':
        return cls(
            word_count=len(content.split()),
            character_count=len(content),
            processed_at=datetime.utcnow()
        )
    
    #convierte los metadatos a un diccionario
    def to_dict(self) -> dict:
        return {
            "word_count": self.word_count,
            "character_count": self.character_count,
            "processed_at": self.processed_at.isoformat()
        }