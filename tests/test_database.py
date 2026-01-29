"""
Script para probar la conexión a la base de datos SQLite.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


print("Probando conexión a la base de datos...\n")

# Test 1: Verificar que SQLAlchemy esté disponible
print("Test 1: Verificando SQLAlchemy...")
try:
    import sqlalchemy
    print(f"SQLAlchemy {sqlalchemy.__version__} encontrado")
except ImportError:
    print("SQLAlchemy no está instalado")
    print("Ejecuta: pip install -r requirements.txt")
    print("O prueba con Docker: docker-compose up --build")
    sys.exit(1)

# Test 2: Import settings and models
print("\n Test 2: Importando configuración y modelos...")
try:
    from Infrastructure.config.settings import settings
    from Infrastructure.database.models import Base, MessageModel
    from Infrastructure.database.connection import engine, create_tables
    
    print(f"Configuración cargada")
    print(f"Database URL: {settings.DATABASE_URL}")
except Exception as e:
    print(f"Error importando: {e}")
    sys.exit(1)

# Test 3: Create tables
print("\n Test 3: Creando tablas en la base de datos...")
try:
    create_tables()
    print("Tablas creadas exitosamente")
except Exception as e:
    print(f"Error creando tablas: {e}")
    sys.exit(1)

# Test 4: Verify table creation
print("\n✓ Test 4: Verificando estructura de tablas...")
try:
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"Tablas encontradas: {tables}")
    
    if "messages" in tables:
        columns = inspector.get_columns("messages")
        print(f"Tabla 'messages' tiene {len(columns)} columnas:")
        for col in columns:
            print(f"     - {col['name']}: {col['type']}")
    else:
        print("Tabla 'messages' no encontrada")
        sys.exit(1)
        
except Exception as e:
    print(f"Error verificando tablas: {e}")
    sys.exit(1)

# Test 5: Test CRUD operations
print("\n Test 5: Probando operaciones CRUD...")
try:
    from sqlalchemy.orm import Session
    from datetime import datetime
    
    # Create session
    session = Session(engine)
    
    # INSERT: Create a test message
    test_message = MessageModel(
        message_id="test-msg-001",
        session_id="test-session-001",
        content="Este es un mensaje de prueba",
        timestamp=datetime.utcnow(),
        sender="user",
        word_count=6,
        character_count=30,
        processed_at=datetime.utcnow()
    )
    
    session.add(test_message)
    session.commit()
    print("INSERT: Mensaje de prueba insertado")
    
    # SELECT: Query the message
    queried_message = session.query(MessageModel).filter_by(
        message_id="test-msg-001"
    ).first()
    
    if queried_message:
        print(f"SELECT: Mensaje recuperado (ID: {queried_message.message_id})")
    else:
        print("SELECT: No se pudo recuperar el mensaje")
    
    # UPDATE: Update the message
    queried_message.content = "Contenido actualizado"
    session.commit()
    print("UPDATE: Mensaje actualizado")
    
    # DELETE: Delete the message
    session.delete(queried_message)
    session.commit()
    print("DELETE: Mensaje eliminado")
    
    # Verify deletion
    count = session.query(MessageModel).count()
    print(f"Verificación: {count} mensajes en la base de datos")
    
    session.close()
    
except Exception as e:
    print(f"Error en operaciones CRUD: {e}")
    session.rollback()
    session.close()
    sys.exit(1)

print("\n" + "=" * 60)
print("Todas las pruebas de base de datos pasaron")
print("=" * 60)
print("\n Resumen:")
print("SQLAlchemy funcionando correctamente")
print("Conexión a SQLite establecida")
print("Tablas creadas con estructura correcta")
print("Operaciones CRUD funcionando")
print("\n La base de datos está lista para usar")
print("\n Siguiente paso:")
print("   docker-compose up --build")
print("   Luego se revisa en: http://localhost:8000/docs")