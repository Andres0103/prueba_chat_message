from fastapi import APIRouter, Depends, status, Query, HTTPException
from typing import Optional

from src.API.v1.schemas.message_schema import (
    MessageCreateSchema,
    MessageResponseSchema,
    PaginatedMessagesSchema,
)

from src.API.v1.schemas.response_schema import SuccessResponse

from src.Application.dtos.message_dto import CreateMessageDTO
from src.Application.dtos.pagination_dto import GetMessagesFilterDTO
from src.Application.use_cases.create_message_use_case import CreateMessageUseCase
from src.Application.use_cases.get_messages_use_case import GetMessagesUseCase

from src.Infrastructure.database.dependencies import get_db
from src.Infrastructure.repositories.message_repository_impl import MessageRepositoryImpl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.Domain.services.content_filter import ContentFilterService
from src.Domain.services.message_processor import MessageProcessor
from src.Infrastructure.database.models import MessageModel

router = APIRouter(prefix="/messages", tags=["Messages"])

# Dependencias de casos de uso. Inyección de dependencias manual.
async def get_create_message_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateMessageUseCase:
    repository = MessageRepositoryImpl(db)
    processor = MessageProcessor()

    return CreateMessageUseCase(
        repository=repository,
        content_filter=ContentFilterService(),
        message_processor=processor,
    )


async def get_get_messages_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetMessagesUseCase:
    repository = MessageRepositoryImpl(db)
    return GetMessagesUseCase(repository=repository)


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)

#función para crear un mensaje con payload y caso de uso
async def create_message(
    payload: MessageCreateSchema,
    use_case: CreateMessageUseCase = Depends(get_create_message_use_case),
):
    try:
        dto = CreateMessageDTO(
            message_id=payload.message_id,
            session_id=payload.session_id,
            content=payload.content,
            timestamp=payload.timestamp,
            sender=payload.sender,
        )

        result = await use_case.execute(dto)

        return SuccessResponse(
            data=MessageResponseSchema(**result.__dict__)
        )
    except ValueError as e:
        # Validación de errores
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Errores inesperados
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get(
    "/{session_id}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)

#Funcion para obtener mensajes con paginación y filtrado
async def get_messages(
    session_id: str,
    limit: int = Query(default=20, ge=1, le=100, description="Límite de mensajes por página"),
    offset: int = Query(default=0, ge=0, description="Desplazamiento para paginación"),
    sender: Optional[str] = Query(default=None, description="Filtro opcional por remitente"),
    use_case: GetMessagesUseCase = Depends(get_get_messages_use_case),
):
    #Obtener mensajes con paginación y filtro opcional por remitente
    try:
        filters = GetMessagesFilterDTO(
            session_id=session_id,
            limit=limit,
            offset=offset,
            sender=sender,
        )

        result = await use_case.execute(filters)
        
        # Convertir DTOs a schemas
        paginated_response = PaginatedMessagesSchema(
            items=[
                MessageResponseSchema(
                    message_id=msg.message_id,
                    session_id=msg.session_id,
                    content=msg.content,
                    timestamp=msg.timestamp,
                    sender=msg.sender,
                    metadata=msg.metadata,
                )
                for msg in result.items
            ],
            limit=result.limit,
            offset=result.offset,
            total=result.total,
        )

        return SuccessResponse(data=paginated_response)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Endpoint de debug para ver todos los mensajes en la BD.
@router.get(
    "/debug/all",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def debug_all_messages(
    db: AsyncSession = Depends(get_db),
):
    stmt = select(MessageModel)
    result = await db.execute(stmt)
    all_messages = result.scalars().all()

    return SuccessResponse(
        data={
            "total_count": len(all_messages),
            "messages": [
                {
                    "message_id": msg.message_id,
                    "session_id": msg.session_id,
                    "content": msg.content,
                    "sender": msg.sender,
                }
                for msg in all_messages
            ]
        }
    )
