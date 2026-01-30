#Importante: Este archivo define el servicio de procesamiento de mensajes en el dominio.
from datetime import datetime
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.message_metadata import MessageMetadata
from src.Application.interfaces.message_processor_interface import MessageProcessorInterface

#Servicio de dominio que procesa mensajes y agrega metadatos
class MessageProcessor(MessageProcessorInterface):

    def process(self, message: MessageEntity) -> MessageEntity:
        # Procesa el mensaje y agrega metadatos como conteo de palabras y caracteres

        word_count = len(message.content.split())
        character_count = len(message.content)

        metadata = MessageMetadata(
            word_count=word_count,
            character_count=character_count,
            processed_at=datetime.utcnow()
        )

        return message.with_metadata(metadata)
