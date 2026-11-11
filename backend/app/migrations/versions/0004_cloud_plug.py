from alembic import op

revision = "0004_cloud_plug"
down_revision = "0003_plug"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TABLE cloud_plug (id INTEGER PRIMARY KEY CHECK (id=1), did TEXT NOT NULL, region TEXT NOT NULL, model TEXT NOT NULL, siid INTEGER NOT NULL, piid INTEGER NOT NULL, user_id TEXT NOT NULL, security TEXT NOT NULL, service_token TEXT NOT NULL)")


def downgrade():
    raise NotImplementedError("Database downgrade is not supported; restore from backup")
