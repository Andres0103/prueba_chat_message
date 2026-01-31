#Test para el endpoint de mensajes de la API
import pytest
from datetime import datetime

#Test para el endpoint POST /api/v1/messages
class TestMessageControllerPostEndpoint:

    #Debe crear un mensaje y devolver HTTP 201 Created
    def test_post_mensaje_con_datos_validos_devuelve_201(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello world",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["message_id"] == "msg-001"
        assert data["data"]["session_id"] == "session-abc"
        assert data["data"]["content"] == "Hello world"
        assert data["data"]["sender"] == "user"

    #Debe devolver respuesta con metadatos (word_count, character_count)
    def test_post_message_returns_response_with_metadata(self, client_with_db):
        """Should return response with metadata (word_count, character_count)."""
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-002",
            "session_id": "session-abc",
            "content": "test message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 201
        data = response.json()
        assert "metadata" in data["data"]
        assert data["data"]["metadata"]["word_count"] == 2
        assert data["data"]["metadata"]["character_count"] == 12

    #Debe devolver HTTP 422 Unprocessable Entity cuando falta message_id
    def test_post_message_missing_message_id_returns_422(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "session_id": "session-abc",
            "content": "Hello",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 422

    #Debe devolver HTTP 400 Bad Request para tipo de remitente no válido
    def test_post_message_with_invalid_sender_returns_400(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello",
            "timestamp": datetime.now().isoformat(),
            "sender": "invalid"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 400

    #Debe devolver HTTP 400 Bad Request cuando el contenido contiene palabras filtradas
    def test_post_message_with_spam_content_returns_400(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-003",
            "session_id": "session-abc",
            "content": "This is spam",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 400

    #Debe devolver HTTP 400 Bad Request cuando el contenido contiene 'malware'
    def test_post_message_with_malware_content_returns_400(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-004",
            "session_id": "session-abc",
            "content": "This contains malware",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 400

    #Debe devolver HTTP 400 Bad Request cuando el contenido contiene 'hack'
    def test_post_message_with_hack_content_returns_400(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-005",
            "session_id": "session-abc",
            "content": "This is a hack attempt",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 400

    #Debe aceptar 'user' como remitente válido
    def test_post_message_with_valid_user_sender(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-006",
            "session_id": "session-abc",
            "content": "User message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 201

    #Debe aceptar 'system' como remitente válido
    def test_post_message_with_valid_system_sender(self, client_with_db):
        # Arrange, preparar los datos necesarios para la prueba
        client = client_with_db
        payload = {
            "message_id": "msg-007",
            "session_id": "session-abc",
            "content": "System message",
            "timestamp": datetime.now().isoformat(),
            "sender": "system"
        }

        # Act, ejecutar la acción que se va a probar
        response = client.post("/api/v1/messages", json=payload)

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 201
        assert response.json()["data"]["sender"] == "system"

#Test para el endpoint GET /api/v1/messages/{session_id}
class TestMessageControllerGetEndpoint:

    #Debe recuperar mensajes para una sesión específica y devolver HTTP 200 OK
    def test_get_messages_for_session_returns_200(self, client_with_db):
        # Arrange, crear un mensaje para la sesión
        client = client_with_db
        create_payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "Hello world",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }
        client.post("/api/v1/messages", json=create_payload)

        # Act, recuperar los mensajes para la sesión
        response = client.get("/api/v1/messages/session-abc")

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "items" in data["data"]
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["message_id"] == "msg-001"

    #Debe devolver un array vacío para una sesión no existente
    def test_get_messages_returns_empty_array_for_non_existent_session(self, client_with_db):
        # Arrange, preparar el cliente
        client = client_with_db

        # Act, intentar recuperar mensajes para una sesión no existente
        response = client.get("/api/v1/messages/nonexistent-session")

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["items"] == []

    #Debe respetar el parámetro de consulta 'limit'
    def test_get_messages_with_limit_query_param(self, client_with_db):
        # Arrange, preparar el cliente
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

        # Act, realizar la solicitud con el parámetro limit
        response = client.get("/api/v1/messages/session-abc?limit=2")

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 2

    #Debe respetar el parámetro de consulta 'offset'
    def test_get_messages_with_offset_query_param(self, client_with_db):
        # Arrange, crear varios mensajes
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

        # Act, realizar la solicitud con el parámetro offset
        response = client.get("/api/v1/messages/session-abc?offset=2")

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1

    #Debe filtrar mensajes por remitente 'user'
    def test_get_messages_with_sender_filter_user(self, client_with_db):
        # Arrange, crear mensajes con diferentes remitentes
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

        # Act, realizar la solicitud con el filtro de remitente
        response = client.get("/api/v1/messages/session-abc?sender=user")

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["sender"] == "user"

    #Debe devolver solo los mensajes de la sesión solicitada
    def test_get_messages_returns_only_requested_session(self, client_with_db):
        # Arrange, crear mensajes para diferentes sesiones
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

        # Act, realizar la solicitud para la sesión 1
        response = client.get("/api/v1/messages/session-1")

        # Assert, verificar que el resultado es el esperado
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        assert data["data"]["items"][0]["session_id"] == "session-1"

    #Debe incluir metadatos en los elementos de la respuesta
    def test_get_messages_includes_metadata_in_response(self, client_with_db):
        # Arrange, crear un mensaje con metadatos
        client = client_with_db
        payload = {
            "message_id": "msg-001",
            "session_id": "session-abc",
            "content": "test message",
            "timestamp": datetime.now().isoformat(),
            "sender": "user"
        }
        client.post("/api/v1/messages", json=payload)

        # Act, realizar la solicitud
        response = client.get("/api/v1/messages/session-abc")

        # Assert, verifica
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["items"]) == 1
        item = data["data"]["items"][0]
        assert "metadata" in item
        assert "word_count" in item["metadata"]
        assert "character_count" in item["metadata"]
        assert item["metadata"]["word_count"] == 2
        assert item["metadata"]["character_count"] == 12
