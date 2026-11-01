from alembic import op

revision = "0002_session_csrf"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE sessions ADD COLUMN csrf_hash TEXT")
    op.execute("DELETE FROM sessions")


def downgrade():
    raise NotImplementedError("Database downgrade is not supported; restore from backup")
