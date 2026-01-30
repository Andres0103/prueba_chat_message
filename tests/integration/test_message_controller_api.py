"""
Integration tests for MessageController API endpoints.
Tests cover: POST/GET endpoints, validation, filtering, pagination, and error handling.
"""
import pytest
from datetime import datetime


class TestMessageControllerPostEndpoint:
    """Tests for POST /api/v1/messages endpoint."""

    def test_post_message_with_valid_data_returns_201(self, client_with_db):
        """Should create a message and return HTTP 201 Created."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello world",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["message_id"] == "msg-001"
        assert data["data"]["session_id"] == "session-abc"
        assert data["data"]["content"] == "Hello world"
        assert data["data"]["sender"] == "user"

    def test_post_message_returns_response_with_metadata(self, client_with_db):
        """Should return response with metadata (word_count, character_count)."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-002",
            "session_id": "session-abc",
            "content": "test message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "metadata" in data["data"]
        assert data["data"]["metadata"]["word_count"] == 2
        assert data["data"]["metadata"]["character_count"] == 12

    def test_post_message_missing_message_id_returns_422(self, client_with_db):
        """Should return HTTP 422 Unprocessable Entity when message_id is missing."""
        # Arrange
        client = client_with_db
        payload = {
            "session_id": "session-abc",
            "content": "Hello",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 422

    def test_post_message_with_invalid_sender_returns_400(self, client_with_db):
        """Should return HTTP 400 Bad Request for invalid sender type."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello",
            "timestamp": datetime.now().isoformat(),
            "sender": "invalid"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 400

    def test_post_message_with_spam_content_returns_400(self, client_with_db):
        """Should return HTTP 400 when content contains filtered words like 'spam'."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-003",
            "session_id": "session-abc",
            "content": "This is spam",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 400

    def test_post_message_with_malware_content_returns_400(self, client_with_db):
        """Should return HTTP 400 when content contains 'malware'."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-004",
            "session_id": "session-abc",
            "content": "This contains malware",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 400

    def test_post_message_with_hack_content_returns_400(self, client_with_db):
        """Should return HTTP 400 when content contains 'hack'."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-005",
            "session_id": "session-abc",
            "content": "This is a hack attempt",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 400

    def test_post_message_with_valid_user_sender(self, client_with_db):
        """Should accept 'user' as valid sender."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-006",
            "session_id": "session-abc",
            "content": "User message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 201

    def test_post_message_with_valid_system_sender(self, client_with_db):
        """Should accept 'system' as valid sender."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-007",
            "session_id": "session-abc",
            "content": "System message",
            "timestamp": datetime.now().isoformat(),
            "sender": "system"
        }

        # Act
        response = client.post("/api/v1/messages", json=payload)

        # Assert
        assert response.status_code == 201
        assert response.json()["data"]["sender"] == "system"


class TestMessageControllerGetEndpoint:
    """Tests for GET /api/v1/messages/{session_id} endpoint."""

    def test_get_messages_for_session_returns_200(self, client_with_db):
        """Should retrieve messages for a specific session."""
        # Arrange - Create a message first
        client = client_with_db
        create_payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello world",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }
        client.post("/api/v1/messages", json=create_payload)

        # Act - Get messages for that session
        response = client.get("/api/v1/messages/session-abc")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "items" in data["data"]
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["message_id"] == "msg-001"

    def test_get_messages_returns_empty_array_for_non_existent_session(self, client_with_db):
        """Should return empty items array for non-existent session."""
        # Arrange
        client = client_with_db

        # Act
        response = client.get("/api/v1/messages/nonexistent-session")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["items"] == []

    def test_get_messages_with_limit_query_param(self, client_with_db):
        """Should respect limit query parameter."""
        # Arrange - Create multiple messages
        client = client_with_db
        for i in range(5):
            payload = {
                "message_id": f"msg-{i:03d}",
                "session_id": "session-abc",
                "content": f"Message {i}",
                "timestamp": datetime.now().isoformat(),
                "sender": "user"
            }
            client.post("/api/v1/messages", json=payload)

        # Act
        response = client.get("/api/v1/messages/session-abc?limit=2")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 2

    def test_get_messages_with_offset_query_param(self, client_with_db):
        """Should respect offset query parameter."""
        # Arrange - Create multiple messages
        client = client_with_db
        for i in range(3):
            payload = {
                "message_id": f"msg-{i:03d}",
                "session_id": "session-abc",
                "content": f"Message {i}",
                "timestamp": datetime.now().isoformat(),
                "sender": "user"
            }
            client.post("/api/v1/messages", json=payload)

        # Act
        response = client.get("/api/v1/messages/session-abc?offset=2")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1

    def test_get_messages_with_sender_filter_user(self, client_with_db):
        """Should filter messages by sender 'user'."""
        # Arrange - Create messages from different senders
        client = client_with_db
        payloads = [
            {
                "message_id": "msg-001",
                "session_id": "session-abc",
                "content": "User message",
                "timestamp": datetime.now().isoformat(),
                "sender": "user"
            },
            {
                "message_id": "msg-002",
                "session_id": "session-abc",
                "content": "System message",
                "timestamp": datetime.now().isoformat(),
                "sender": "system"
            }
        ]
        for payload in payloads:
            client.post("/api/v1/messages", json=payload)

        # Act
        response = client.get("/api/v1/messages/session-abc?sender=user")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["sender"] == "user"

    def test_get_messages_returns_only_requested_session(self, client_with_db):
        """Should only return messages from the requested session."""
        # Arrange - Create messages in different sessions
        client = client_with_db
        payloads = [
            {
                "message_id": "msg-001",
                "session_id": "session-1",
                "content": "Session 1 message",
                "timestamp": datetime.now().isoformat(),
                "sender": "user"
            },
            {
                "message_id": "msg-002",
                "session_id": "session-2",
                "content": "Session 2 message",
                "timestamp": datetime.now().isoformat(),
                "sender": "user"
            }
        ]
        for payload in payloads:
            client.post("/api/v1/messages", json=payload)

        # Act
        response = client.get("/api/v1/messages/session-1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["session_id"] == "session-1"

    def test_get_messages_includes_metadata_in_response(self, client_with_db):
        """Should include metadata in response items."""
        # Arrange
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "test message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }
        client.post("/api/v1/messages", json=payload)

        # Act
        response = client.get("/api/v1/messages/session-abc")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        item = data["data"]["items"][0]
        assert "metadata" in item
        assert "word_count" in item["metadata"]
        assert "character_count" in item["metadata"]
        assert item["metadata"]["word_count"] == 2
        assert item["metadata"]["character_count"] == 12
