import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from app import db


class MigrationTests(unittest.TestCase):
    def test_existing_users_are_preserved(self):
        original = db.DB_PATH
        with tempfile.TemporaryDirectory() as temp:
            db.DB_PATH = Path(temp) / "existing.sqlite3"
            try:
                with closing(sqlite3.connect(db.DB_PATH)) as conn:
                    with conn:
                        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL, enabled INTEGER NOT NULL DEFAULT 1)")
                        conn.execute("INSERT INTO users(username,password_hash,role) VALUES('existing','hash','admin')")
                        conn.execute("CREATE TABLE sessions (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL, expires_at REAL NOT NULL)")
                        conn.execute("INSERT INTO sessions VALUES('old-token', 1, 9999999999)")
                db.initialize()
                with db.connect() as conn:
                    self.assertEqual(conn.execute("SELECT username FROM users").fetchone()[0], "existing")
                    self.assertEqual(conn.execute("SELECT version_num FROM alembic_version").fetchone()[0], "0002_session_csrf")
                    self.assertEqual(conn.execute("SELECT day_minutes FROM server_policy").fetchone()[0], 90)
                    self.assertEqual(conn.execute("SELECT count(*) FROM sessions").fetchone()[0], 0)
            finally:
                db.DB_PATH = original


if __name__ == "__main__":
    unittest.main()
