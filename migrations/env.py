from __future__ import with_statement
import logging
import logging.config
from alembic import context
from sqlalchemy import engine_from_config, pool
from fast_zero.models import table_registry  # Altere conforme necessário

# Configuração do Alembic
config = context.config

# Configurações de logging
logging.config.fileConfig(config.config_file_name)

# Adicione o objeto MetaData do seu modelo
target_metadata = table_registry.metadata

def run_migrations_offline():
    """Executa migrações em modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Executa migrações em modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
