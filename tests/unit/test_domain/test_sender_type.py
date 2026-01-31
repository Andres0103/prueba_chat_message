#test para el value object SenderType
from src.Domain.value_objects.sender_type import SenderType

#test para verificar los valores del enum SenderType
def test_sender_type_values():
    assert SenderType.USER.value == "user"
    assert SenderType.SYSTEM.value == "system"
