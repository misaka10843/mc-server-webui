from alembic import context


def run_migrations_online():
    connection = context.config.attributes["connection"]
    context.configure(connection=connection, target_metadata=None)
    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()
