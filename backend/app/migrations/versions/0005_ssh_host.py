from alembic import op

revision = "0005_ssh_host"
down_revision = "0004_cloud_plug"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TABLE ssh_host (id INTEGER PRIMARY KEY CHECK (id=1), config TEXT NOT NULL)")


def downgrade():
    raise NotImplementedError("Database downgrade is not supported; restore from backup")
