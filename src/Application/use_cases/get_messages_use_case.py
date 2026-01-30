#Importante: Este archivo implementa el caso de uso para obtener mensajes con paginación y filtrado.
from src.Application.interfaces.message_repository_interface import MessageRepositoryInterface
from src.Application.dtos.message_dto import MessageDTO
from src.Application.dtos.pagination_dto import GetMessagesFilterDTO, PaginationDTO

#Caso de uso para obtener mensajes de una sesión con paginación y filtrado
class GetMessagesUseCase:

    def __init__(self, repository: MessageRepositoryInterface):
        self.repository = repository

    def execute(self, filters: GetMessagesFilterDTO) -> PaginationDTO[MessageDTO]:
        """
        Ejecuta el caso de uso de obtención de mensajes.

        Args:
            filters: DTO con los parámetros de búsqueda y paginación

        Returns:
            DTO de paginación con los mensajes encontrados
        """

        messages = self.repository.get_by_session(
            session_id=filters.session_id,
            limit=filters.limit,
            offset=filters.offset,
            sender=filters.sender,
        )

        # Obtener el total de mensajes (con los mismos filtros)
        total = self.repository.count_by_session(
            session_id=filters.session_id,
            sender=filters.sender,
        )

        # Convertir entidades a DTOs
        message_dtos = [
            MessageDTO(
                message_id=msg.message_id,
                session_id=msg.session_id,
                content=msg.content,
                timestamp=msg.timestamp,
                sender=msg.sender.value,
                metadata=msg.metadata.__dict__ if msg.metadata else None,
            )
            for msg in messages
        ]
        return PaginationDTO(
            items=message_dtos,
            limit=filters.limit,
            offset=filters.offset,
            total=total,
        )
