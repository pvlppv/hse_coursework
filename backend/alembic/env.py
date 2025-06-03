import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from base import Base
from database import engine
from settings import get_settings

cfg = get_settings()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", cfg.database_url)
print(f"Database URL: {cfg.database_url}")
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    print(f"Setting up offline migrations with URL: {cfg.database_url}")
    config.set_main_option("sqlalchemy.url", cfg.database_url)
    url = config.get_main_option("sqlalchemy.url")
    print(f"Configured URL for offline mode: {url}")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # handle async engine
    connectable = engine

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations():
    """Run migrations either offline or online."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())

run_migrations()