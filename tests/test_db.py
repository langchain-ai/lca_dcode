import sqlite3

import pytest

from ledger import db


def test_migrate_creates_expected_tables(conn):
    tables = {
        row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    assert {"categories", "transactions", "schema_migrations"} <= tables


def test_migrate_is_idempotent(conn):
    assert db.migrate(conn) == []


def test_foreign_keys_are_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO transactions (occurred_on, description, amount_cents, category_id)"
            " VALUES ('2026-01-01', 'x', -100, 9999)"
        )
