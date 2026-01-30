from unittest.mock import Mock
from src.Application.use_cases.get_messages_use_case import GetMessagesUseCase
from src.Application.dtos.pagination_dto import PaginationDTO

from src.Application.dtos.pagination_dto import GetMessagesFilterDTO

def test_get_messages_returns_list(repository_mock):
    use_case = GetMessagesUseCase(repository_mock)
    filters = GetMessagesFilterDTO(
        session_id="session-1",
        limit=10,
        offset=0
    )

    result = use_case.execute(filters)

    assert isinstance(result.items, list)
    assert result.limit == 10
    assert result.offset == 0

