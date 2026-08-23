"""SQLite connection handling and a tiny forward-only migration runner.

There is no ORM here on purpose. Repositories write SQL; nothing else does.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def connect(database_path: str | Path) -> sqlite3.Connection:
    """Open a connection with the settings the rest of the app assumes."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> list[str]:
    """Apply every .sql file in migrations/ that hasn't run yet.

    Migrations run in filename order and are recorded in schema_migrations, so
    calling this repeatedly is safe. Returns the names that were applied.
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            name       TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()

    already_applied = {row["name"] for row in conn.execute("SELECT name FROM schema_migrations")}

    applied_now: list[str] = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if path.name in already_applied:
            continue
        conn.executescript(path.read_text(encoding="utf-8"))
        conn.execute("INSERT INTO schema_migrations (name) VALUES (?)", (path.name,))
        conn.commit()
        applied_now.append(path.name)

    return applied_now
