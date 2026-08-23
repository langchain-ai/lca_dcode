"""Data access for transactions.

This module is the reference example for how a repository is written in this
codebase. It imports nothing from FastAPI and knows nothing about HTTP.
"""

from __future__ import annotations

import sqlite3
from typing import Any

SELECT_WITH_CATEGORY = """
    SELECT t.id,
           t.occurred_on,
           t.description,
           t.amount_cents,
           t.category_id,
           t.note,
           t.created_at,
           c.name AS category_name
      FROM transactions t
      LEFT JOIN categories c ON c.id = t.category_id
"""


def _to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def list_transactions(
    conn: sqlite3.Connection,
    *,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Return transactions, newest first.

    Filtering by text, category, or date range is not supported yet.
    """
    rows = conn.execute(
        SELECT_WITH_CATEGORY + " ORDER BY t.occurred_on DESC, t.id DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return [dict(row) for row in rows]


def get_transaction(conn: sqlite3.Connection, transaction_id: int) -> dict[str, Any] | None:
    """Return one transaction, or None if it doesn't exist."""
    row = conn.execute(
        SELECT_WITH_CATEGORY + " WHERE t.id = ?",
        (transaction_id,),
    ).fetchone()
    return _to_dict(row)


def create_transaction(
    conn: sqlite3.Connection,
    *,
    occurred_on: str,
    description: str,
    amount_cents: int,
    category_id: int | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    """Insert a transaction and return it as stored."""
    cursor = conn.execute(
        """
        INSERT INTO transactions (occurred_on, description, amount_cents, category_id, note)
        VALUES (?, ?, ?, ?, ?)
        """,
        (occurred_on, description, amount_cents, category_id, note),
    )
    conn.commit()
    created = get_transaction(conn, int(cursor.lastrowid))
    assert created is not None
    return created


def update_transaction(
    conn: sqlite3.Connection,
    transaction_id: int,
    **fields: Any,
) -> dict[str, Any] | None:
    """Update the given columns. Returns the updated row, or None if missing.

    Only known columns are accepted; anything else raises ValueError so a typo
    fails loudly instead of silently doing nothing.
    """
    allowed = {"occurred_on", "description", "amount_cents", "category_id", "note"}
    unknown = set(fields) - allowed
    if unknown:
        raise ValueError(f"unknown transaction columns: {sorted(unknown)}")
    if not fields:
        return get_transaction(conn, transaction_id)

    assignments = ", ".join(f"{column} = ?" for column in fields)
    conn.execute(
        f"UPDATE transactions SET {assignments} WHERE id = ?",  # noqa: S608 - columns allow-listed
        (*fields.values(), transaction_id),
    )
    conn.commit()
    return get_transaction(conn, transaction_id)


def delete_transaction(conn: sqlite3.Connection, transaction_id: int) -> bool:
    """Delete a transaction. Returns True if a row was removed."""
    cursor = conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    return cursor.rowcount > 0


def total_cents(conn: sqlite3.Connection) -> int:
    """Net total across every transaction ever recorded."""
    row = conn.execute("SELECT COALESCE(SUM(amount_cents), 0) AS total FROM transactions").fetchone()
    return int(row["total"])


def count_transactions(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) AS n FROM transactions").fetchone()
    return int(row["n"])
