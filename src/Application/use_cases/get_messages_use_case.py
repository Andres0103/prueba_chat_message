#Importante: Este archivo implementa el caso de uso para obtener mensajes con paginación y filtrado.
from src.Application.interfaces.message_repository_interface import MessageRepositoryInterface
from src.Application.dtos.message_dto import MessageDTO
from src.Application.dtos.pagination_dto import GetMessagesFilterDTO, PaginationDTO

#Caso de uso para obtener mensajes de una sesión con paginación y filtrado
class GetMessagesUseCase:

    def __init__(self, repository: MessageRepositoryInterface):
        self.repository = repository

    async def execute(self, filters: GetMessagesFilterDTO) -> PaginationDTO[MessageDTO]:
        """
        Ejecuta el caso de uso de obtención de mensajes.

        Args:
            filters: DTO con los parámetros de búsqueda y paginación

        Returns:
            DTO de paginación con los mensajes encontrados
        """
        if not filters.session_id or not filters.session_id.strip():
            raise ValueError("session_id no puede estar vacío")
        
        if filters.limit and filters.limit < 0:
            raise ValueError("limit debe ser positivo")
        
        if filters.offset is not None and filters.offset < 0:
            raise ValueError("offset debe ser no negativo")
        
        # Aplicar valor por defecto de límite si es 0
        limit = filters.limit if filters.limit and filters.limit > 0 else 10
        
        # Asegurar que el límite no exceda 100
        limit = min(limit, 100)

        # Si se pide filtrar por `sender` y la sesión ya existe pero el sender
        # no tiene mensajes en esa sesión, consideramos esto una validación
        # y devolvemos un error claro en lugar de una lista vacía.
        if filters.sender:
            session_total = await self.repository.count_by_session(session_id=filters.session_id)
            if session_total > 0:
                sender_total = await self.repository.count_by_session(
                    session_id=filters.session_id, sender=filters.sender
                )
                if sender_total == 0:
                    raise ValueError(
                        f"sender '{filters.sender}' no pertenece a la sesión '{filters.session_id}'"
                    )

        messages = await self.repository.get_by_session(
            session_id=filters.session_id,
            limit=limit,
            offset=filters.offset or 0,
            sender=filters.sender,
        )

        # Obtener el total de mensajes (con los mismos filtros)
        total = await self.repository.count_by_session(
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
            limit=limit,
            offset=filters.offset or 0,
            total=total,
        )
