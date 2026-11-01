from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
        enabled INTEGER NOT NULL DEFAULT 1
    )""")
    op.execute("""CREATE TABLE IF NOT EXISTS sessions (
        token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        expires_at REAL NOT NULL
    )""")
    op.execute("""CREATE TABLE IF NOT EXISTS audit_events (
        id INTEGER PRIMARY KEY, created_at REAL NOT NULL, user_id INTEGER,
        action TEXT NOT NULL, detail TEXT NOT NULL
    )""")
    op.execute("""CREATE TABLE IF NOT EXISTS operations (
        id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, kind TEXT NOT NULL,
        status TEXT NOT NULL, detail TEXT NOT NULL, created_at REAL NOT NULL, updated_at REAL NOT NULL
    )""")
    op.execute("""CREATE TABLE IF NOT EXISTS server_policy (
        id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL,
        enabled INTEGER NOT NULL, day_minutes INTEGER NOT NULL, night_minutes INTEGER NOT NULL,
        night_start TEXT NOT NULL, day_start TEXT NOT NULL
    )""")
    op.execute("INSERT OR IGNORE INTO server_policy VALUES(1, 1, 0, 90, 30, '23:30', '09:00')")
    op.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_events(created_at)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_operations_created ON operations(created_at)")


def downgrade():
    raise NotImplementedError("Database downgrade is not supported; restore from backup")
