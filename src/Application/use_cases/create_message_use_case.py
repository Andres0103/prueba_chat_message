#Importante: Este archivo implementa el caso de uso para crear un mensaje.

from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Application.dtos.message_dto import CreateMessageDTO, MessageResponseDTO
from src.Application.interfaces.message_repository_interface import MessageRepositoryInterface
from src.Application.interfaces.content_filter_interface import ContentFilterInterface
from src.Application.interfaces.message_processor_interface import MessageProcessorInterface

#Clase que implementa el caso de uso para crear un mensaje. 
#Orquesta las reglas del dominio y la persistencia.
class CreateMessageUseCase:

    def __init__(
        self,
        repository: MessageRepositoryInterface,
        content_filter: ContentFilterInterface,
        message_processor: MessageProcessorInterface,
    ):
        self.repository = repository
        self.content_filter = content_filter
        self.message_processor = message_processor

    def execute(self, dto: CreateMessageDTO) -> MessageResponseDTO:
        """
        Ejecuta el flujo de creación del mensaje.
        """
        # Convertir DTO a entidad
        sender = SenderType(dto.sender)
        # Aplicar filtro de contenido
        filtered_content = self.content_filter.filter(dto.content)
        # Crear entidad de mensaje
        message = MessageEntity(
            message_id=dto.message_id,
            session_id=dto.session_id,
            content=filtered_content,
            timestamp=dto.timestamp,
            sender=sender
        )
        # Procesar el mensaje (lógica de negocio adicional)
        processed_message = self.message_processor.process(message)

        saved_message = self.repository.save(processed_message)
        # Convertir entidad guardada a DTO de respuesta
        return MessageResponseDTO(
            message_id=saved_message.message_id,
            session_id=saved_message.session_id,
            content=saved_message.content,
            timestamp=saved_message.timestamp,
            sender=saved_message.sender.value,
            metadata=saved_message.metadata.to_dict() if saved_message.metadata else None
        )
