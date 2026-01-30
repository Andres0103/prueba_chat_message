from src.Domain.value_objects.message_metadata import MessageMetadata


def test_metadata_word_count():
    metadata = MessageMetadata.from_content("Hello world")
    assert metadata.word_count == 2


def test_metadata_empty_content():
    metadata = MessageMetadata.from_content("")
    assert metadata.word_count == 0
