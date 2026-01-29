from fastapi import APIRouter, Depends, HTTPException, status

from src.API.v1.schemas.message_schema import (
    MessageCreateSchema,
    MessageResponseSchema,
)

from src.API.v1.schemas.error_schema import ErrorResponse
from src.API.v1.schemas.response_schema import SuccessResponse

from src.Application.dtos.message_dto import CreateMessageDTO
from src.Application.use_cases.create_message_use_case import CreateMessageUseCase

from src.Infrastructure.database.connection import get_db as get_db_session
from src.Infrastructure.repositories.message_repository_impl import MessageRepositoryImpl
from src.Domain.services.content_filter import ContentFilterService
from src.Domain.services.message_processor import MessageProcessor

router = APIRouter(prefix="/api/messages", tags=["Messages"])

def get_create_message_use_case(
    db=Depends(get_db_session),
) -> CreateMessageUseCase:
    repository = MessageRepositoryImpl(db)
    content_filter = ContentFilterService()
    processor = MessageProcessor()

    return CreateMessageUseCase(
        repository=repository,
        content_filter=content_filter,
        message_processor=processor,
    )

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
