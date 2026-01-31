# Test para el endpoint de mensajes de la API
import pytest
from datetime import datetime

# ensure pytest-asyncio applies to module async tests
pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
class TestMessageControllerPostEndpoint:

    async def test_post_mensaje_con_datos_validos_devuelve_201(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello world",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["message_id"] == "msg-001"
        assert data["data"]["session_id"] == "session-abc"
        assert data["data"]["content"] == "Hello world"
        assert data["data"]["sender"] == "user"

    async def test_post_message_returns_response_with_metadata(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-002",
            "session_id": "session-abc",
            "content": "test message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert "metadata" in data["data"]
        assert data["data"]["metadata"]["word_count"] == 2
        assert data["data"]["metadata"]["character_count"] == 12

    async def test_post_message_missing_message_id_returns_422(self, client_with_db):
        client = client_with_db
        payload = {
            "session_id": "session-abc",
            "content": "Hello",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 422

    async def test_post_message_with_invalid_sender_returns_400(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello",
            "timestamp": datetime.now().isoformat(),
            "sender": "invalid",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 400

    async def test_post_message_with_spam_content_returns_400(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-003",
            "session_id": "session-abc",
            "content": "This is spam",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 400

    async def test_post_message_with_malware_content_returns_400(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-004",
            "session_id": "session-abc",
            "content": "This contains malware",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 400

    async def test_post_message_with_hack_content_returns_400(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-005",
            "session_id": "session-abc",
            "content": "This is a hack attempt",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 400

    async def test_post_message_with_valid_user_sender(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-006",
            "session_id": "session-abc",
            "content": "User message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 201

    async def test_post_message_with_valid_system_sender(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-007",
            "session_id": "session-abc",
            "content": "System message",
            "timestamp": datetime.now().isoformat(),
            "sender": "system",
        }

        response = await client.post("/api/v1/messages", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["sender"] == "system"


@pytest.mark.asyncio
class TestMessageControllerGetEndpoint:

    async def test_get_messages_for_session_returns_200(self, client_with_db):
        client = client_with_db
        create_payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello world",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }
        await client.post("/api/v1/messages", json=create_payload)

        response = await client.get("/api/v1/messages/session-abc")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "items" in data["data"]
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["message_id"] == "msg-001"

    async def test_get_messages_returns_empty_array_for_non_existent_session(self, client_with_db):
        client = client_with_db

        response = await client.get("/api/v1/messages/nonexistent-session")

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["items"] == []

    async def test_get_messages_with_limit_query_param(self, client_with_db):
        client = client_with_db
        for i in range(5):
            payload = {
                "message_id": f"msg-{i:03d}",
                "session_id": "session-abc",
                "content": f"Message {i}",
                "timestamp": datetime.now().isoformat(),
                "sender": "user",
            }
            await client.post("/api/v1/messages", json=payload)

        response = await client.get("/api/v1/messages/session-abc?limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 2

    async def test_get_messages_with_offset_query_param(self, client_with_db):
        client = client_with_db
        for i in range(3):
            payload = {
                "message_id": f"msg-{i:03d}",
                "session_id": "session-abc",
                "content": f"Message {i}",
                "timestamp": datetime.now().isoformat(),
                "sender": "user",
            }
            await client.post("/api/v1/messages", json=payload)

        response = await client.get("/api/v1/messages/session-abc?offset=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1

    async def test_get_messages_with_sender_filter_user(self, client_with_db):
        client = client_with_db
        payloads = [
            {
                "message_id": "msg-001",
                "session_id": "session-abc",
                "content": "User message",
                "timestamp": datetime.now().isoformat(),
                "sender": "user",
            },
            {
                "message_id": "msg-002",
                "session_id": "session-abc",
                "content": "System message",
                "timestamp": datetime.now().isoformat(),
                "sender": "system",
            },
        ]
        for payload in payloads:
            await client.post("/api/v1/messages", json=payload)

        response = await client.get("/api/v1/messages/session-abc?sender=user")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["sender"] == "user"

    async def test_get_messages_returns_only_requested_session(self, client_with_db):
        client = client_with_db
        payloads = [
            {
                "message_id": "msg-001",
                "session_id": "session-1",
                "content": "Session 1 message",
                "timestamp": datetime.now().isoformat(),
                "sender": "user",
            },
            {
                "message_id": "msg-002",
                "session_id": "session-2",
                "content": "Session 2 message",
                "timestamp": datetime.now().isoformat(),
                "sender": "user",
            },
        ]
        for payload in payloads:
            await client.post("/api/v1/messages", json=payload)

        response = await client.get("/api/v1/messages/session-1")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["session_id"] == "session-1"

    async def test_get_messages_includes_metadata_in_response(self, client_with_db):
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "test message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user",
        }
        await client.post("/api/v1/messages", json=payload)

        response = await client.get("/api/v1/messages/session-abc")

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        item = data["data"]["items"][0]
        assert "metadata" in item
        assert "word_count" in item["metadata"]
        assert "character_count" in item["metadata"]
        assert item["metadata"]["word_count"] == 2
        assert item["metadata"]["character_count"] == 12
