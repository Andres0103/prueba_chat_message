from src.Domain.value_objects.sender_type import SenderType


def test_sender_type_values():
    assert SenderType.USER.value == "user"
    assert SenderType.SYSTEM.value == "system"
