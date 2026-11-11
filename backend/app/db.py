import argparse
import os
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

from argon2 import PasswordHasher
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

DB_PATH = Path(os.environ.get("MCWEB_DB", "mcweb.sqlite3"))
passwords = PasswordHasher()


@contextmanager
def connect():
    db = sqlite3.connect(DB_PATH, timeout=10)
    try:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA foreign_keys=ON")
        with db:
            yield db
    finally:
        db.close()


def initialize():
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
    engine = create_engine(URL.create("sqlite", database=str(DB_PATH)))
    try:
        with engine.begin() as connection:
            config.attributes["connection"] = connection
            command.upgrade(config, "head")
    finally:
        engine.dispose()
    with connect() as db:
        db.execute("UPDATE operations SET status='unknown', detail='Backend restarted; check current status', updated_at=? WHERE status='running'", (time.time(),))


def main():
    import getpass
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()
    password = getpass.getpass("Password: ")
    if len(password) < 8:
        raise SystemExit("Password must contain at least 8 characters")
    initialize()
    with connect() as db:
        if db.execute("SELECT 1 FROM users WHERE role='admin'").fetchone():
            raise SystemExit("Administrator already exists")
        db.execute("INSERT INTO users(username, password_hash, role) VALUES(?,?,?)", (args.username, passwords.hash(password), "admin"))
    print("Administrator created")


if __name__ == "__main__":
    main()
