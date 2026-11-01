from alembic import op

revision = "0003_plug"
down_revision = "0002_session_csrf"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TABLE plug_config (id INTEGER PRIMARY KEY CHECK (id=1), ip TEXT NOT NULL, token TEXT NOT NULL, model TEXT NOT NULL, siid INTEGER NOT NULL, piid INTEGER NOT NULL)")


def downgrade():
    raise NotImplementedError("Database downgrade is not supported; restore from backup")
