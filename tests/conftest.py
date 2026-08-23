"""Shared fixtures.

Every test gets its own database in a temp directory, so tests never touch the
ledger.db in the project root.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator

import pytest


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "test.db"
    monkeypatch.setenv("LEDGER_DATABASE_PATH", str(path))
    return path


@pytest.fixture
def conn(db_path) -> Iterator[sqlite3.Connection]:
    """A migrated, empty database. Use this for repository tests."""
    from ledger import db

    connection = db.connect(db_path)
    db.migrate(connection)
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def client(db_path):
    """A TestClient wired to a fresh database. Use this for router tests."""
    from fastapi.testclient import TestClient

    from ledger.main import create_app

    with TestClient(create_app()) as test_client:
        yield test_client


@pytest.fixture
def sample_categories(conn) -> dict[str, int]:
    conn.executemany(
        "INSERT INTO categories (name, kind) VALUES (?, ?)",
        [("Groceries", "expense"), ("Salary", "income")],
    )
    conn.commit()
    return {row["name"]: row["id"] for row in conn.execute("SELECT id, name FROM categories")}
