import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ✅ Ensure parent directory (where `app/` lives) is in Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ✅ Load .env file
load_dotenv()

# ✅ Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Import SQLAlchemy Base and models
from app.db.session import Base
from app.db.models import transaction, user  # <-- these exist in your service

# ✅ Use DB_URL from environment (.env)
database_url = os.getenv("DB_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
else:
    raise ValueError("❌ DB_URL not found in .env — please check your file.")

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
