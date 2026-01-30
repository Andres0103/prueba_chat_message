from fastapi import APIRouter, Depends, status, Query, HTTPException
from typing import Optional

from src.API.v1.schemas.message_schema import (
    MessageCreateSchema,
    MessageResponseSchema,
    PaginatedMessagesSchema,
)

from src.API.v1.schemas.response_schema import SuccessResponse, ErrorResponse

from src.Application.dtos.message_dto import CreateMessageDTO
from src.Application.dtos.pagination_dto import GetMessagesFilterDTO
from src.Application.use_cases.create_message_use_case import CreateMessageUseCase
from src.Application.use_cases.get_messages_use_case import GetMessagesUseCase

from src.Infrastructure.database.connection import get_db
from src.Infrastructure.repositories.message_repository_impl import MessageRepositoryImpl
from src.Domain.services.content_filter import ContentFilterService
from src.Domain.services.message_processor import MessageProcessor

router = APIRouter(prefix="/messages", tags=["Messages"])

def get_create_message_use_case(
    db=Depends(get_db),
) -> CreateMessageUseCase:
    repository = MessageRepositoryImpl(db)
    processor = MessageProcessor()

    return CreateMessageUseCase(
        repository=repository,
        content_filter=ContentFilterService(),
        message_processor=processor,
    )


def get_get_messages_use_case(
    db=Depends(get_db),
) -> GetMessagesUseCase:
    repository = MessageRepositoryImpl(db)
    return GetMessagesUseCase(repository=repository)


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
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

        result = use_case.execute(dto)

        return SuccessResponse(
            data=MessageResponseSchema(**result.__dict__)
        )
    except ValueError as e:
        # Content filtering or validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Unexpected errors
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
def get_messages(
    session_id: str,
    limit: int = Query(default=20, ge=1, le=100, description="Límite de mensajes por página"),
    offset: int = Query(default=0, ge=0, description="Desplazamiento para paginación"),
    sender: Optional[str] = Query(default=None, description="Filtro opcional por remitente"),
    use_case: GetMessagesUseCase = Depends(get_get_messages_use_case),
):
    """
    Obtiene todos los mensajes para una sesión dada.
    
    Soporta:
    - Paginación mediante limit y offset
    - Filtrado por remitente
    """
    try:
        filters = GetMessagesFilterDTO(
            session_id=session_id,
            limit=limit,
            offset=offset,
            sender=sender,
        )

        result = use_case.execute(filters)
        
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
            detail="An unexpected error occurred"
        )


@router.get(
    "/debug/all",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
def debug_all_messages(
    db = Depends(get_db),
):
    """
    Endpoint de debug para ver todos los mensajes en la BD.
    """
    from src.Infrastructure.database.models import MessageModel
    
    all_messages = db.query(MessageModel).all()
    
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
