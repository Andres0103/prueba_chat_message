"""Alembic environment configuration."""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from pathlib import Path

# -------------------------------------------------------------------------
# Ajustar el path para que Alembic encuentre el código del proyecto
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# -------------------------------------------------------------------------
# Importar settings y Base (ESTO ES CLAVE PARA AUTOGENERATE)
# -------------------------------------------------------------------------

from src.Infrastructure.config.settings import settings
from src.Infrastructure.database.models import Base, MessageModel

# IMPORTANTE:
# Hay que importar explícitamente los modelos para que SQLAlchemy
# los registre en Base.metadata
from src.Infrastructure.database.models import MessageModel

# -------------------------------------------------------------------------
# Configuración de Alembic
# -------------------------------------------------------------------------
config = context.config

# Sobrescribimos la URL de la DB con la de settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata que Alembic usará para comparar modelos vs DB
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {
            "sqlalchemy.url": settings.DATABASE_URL
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
