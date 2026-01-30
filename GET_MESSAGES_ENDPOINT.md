# Endpoint GET `/api/messages/{session_id}` - Documentación

## Descripción
Obtiene todos los mensajes para una sesión dada con soporte para **paginación** y **filtrado por remitente**.

## Ruta
```
GET /api/messages/{session_id}
```

## Parámetros

### Path Parameters
- `session_id` (string, requerido): ID de la sesión para la cual se desean obtener los mensajes
  - Ejemplo: `session-abcdef`

### Query Parameters
- `limit` (integer, opcional): Número máximo de mensajes a retornar por página
  - Por defecto: `20`
  - Rango válido: `1` a `100`
  
- `offset` (integer, opcional): Número de mensajes a saltar (para paginación)
  - Por defecto: `0`
  - Mínimo: `0`
  
- `sender` (string, opcional): Filtro para obtener solo mensajes de un remitente específico
  - Ejemplo: `user`, `bot`, `assistant`
  - Si se omite, se retornan mensajes de todos los remitentes

## Respuesta (200 OK)

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "message_id": "msg-123456",
        "session_id": "session-abcdef",
        "content": "Hola, ¿cómo puedo ayudarte?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "bot",
        "metadata": {
          "word_count": 6,
          "character_count": 33,
          "processed_at": "2023-06-15T14:30:01Z"
        }
      },
      {
        "message_id": "msg-123457",
        "session_id": "session-abcdef",
        "content": "Necesito ayuda con mi cuenta",
        "timestamp": "2023-06-15T14:31:00Z",
        "sender": "user",
        "metadata": {
          "word_count": 5,
          "character_count": 29,
          "processed_at": "2023-06-15T14:31:01Z"
        }
      }
    ],
    "limit": 20,
    "offset": 0,
    "total": 2
  }
}
```

## Ejemplos de Uso

### 1. Obtener todos los mensajes de una sesión (paginación por defecto)
```bash
curl -X GET "http://localhost:8000/api/messages/session-abcdef" \
  -H "Content-Type: application/json"
```

### 2. Obtener mensajes con paginación personalizada
```bash
curl -X GET "http://localhost:8000/api/messages/session-abcdef?limit=10&offset=0" \
  -H "Content-Type: application/json"
```

### 3. Obtener solo mensajes de un remitente específico
```bash
curl -X GET "http://localhost:8000/api/messages/session-abcdef?sender=user" \
  -H "Content-Type: application/json"
```

### 4. Combinación: Filtrar por remitente y paginar
```bash
curl -X GET "http://localhost:8000/api/messages/session-abcdef?sender=bot&limit=10&offset=20" \
  -H "Content-Type: application/json"
```

### 5. Usando Python requests
```python
import requests

# Obtener mensajes de la sesión con filtros
response = requests.get(
    "http://localhost:8000/api/messages/session-abcdef",
    params={
        "limit": 20,
        "offset": 0,
        "sender": "user"  # opcional
    }
)

data = response.json()
print(f"Total de mensajes: {data['data']['total']}")
print(f"Mensajes en esta página: {len(data['data']['items'])}")

for message in data['data']['items']:
    print(f"{message['sender']}: {message['content']}")
```

## Características Implementadas

✅ **Paginación (limit/offset)**: Controla la cantidad de resultados por página
- Limite máximo de 100 mensajes por solicitud
- Offset para navegar entre páginas

✅ **Filtrado por remitente**: Obtén solo los mensajes de un remitente específico
- El filtro respeta la paginación (el total se calcula después del filtrado)

✅ **Ordenamiento**: Los mensajes se retornan ordenados por timestamp ascendente
- Los mensajes más antiguos aparecen primero

✅ **Metadata**: Cada mensaje incluye información de procesamiento (word_count, character_count, etc.)

## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `400 Bad Request`: Parámetros inválidos (limit/offset fuera de rango)
- `422 Unprocessable Entity`: Error de validación en los parámetros

## Notas de Implementación

- La endpoint está completamente integrada con la arquitectura hexagonal del proyecto
- Utiliza el caso de uso `GetMessagesUseCase` para orquestar la lógica de negocio
- El repositorio implementa paginación eficiente a nivel de base de datos
- Todos los parámetros son validados por Pydantic antes de ser procesados
