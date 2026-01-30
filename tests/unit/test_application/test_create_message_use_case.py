from unittest.mock import Mock
from src.Application.use_cases.create_message_use_case import CreateMessageUseCase
from src.Application.dtos.message_dto import MessageDTO

def test_create_message_success():
    repository = Mock()
    content_filter = Mock()
    message_processor = Mock()

    content_filter.filter_content.return_value = (True, "")
    message_processor.process.return_value = "processed content"

    use_case = CreateMessageUseCase(
        repository=repository,
        content_filter=content_filter,
        message_processor=message_processor
    )

    request = MessageDTO(
    session_id="session-1",
    content="hello",
    sender="USER"
    )

    result = use_case.execute(request)

    assert result is not None
