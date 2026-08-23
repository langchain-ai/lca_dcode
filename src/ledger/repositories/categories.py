"""Data access for categories.

NOT IMPLEMENTED. The categories table exists and transactions already point at
it, but nothing in the app can create, rename, or delete a category yet.

The signatures below are the contract the rest of the app expects. Fill them in
following the patterns in transactions.py.
"""

from __future__ import annotations

import sqlite3
from typing import Any

_NOT_BUILT = "Category management is not built yet."


def list_categories(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return every category ordered by name."""
    raise NotImplementedError(_NOT_BUILT)


def get_category(conn: sqlite3.Connection, category_id: int) -> dict[str, Any] | None:
    """Return one category, or None if it doesn't exist."""
    raise NotImplementedError(_NOT_BUILT)


def create_category(conn: sqlite3.Connection, *, name: str, kind: str) -> dict[str, Any]:
    """Insert a category.

    `kind` is either "expense" or "income" — the CHECK constraint in
    001_initial.sql enforces that. Names are unique; a duplicate should surface
    as a 409 at the router, not a 500.
    """
    raise NotImplementedError(_NOT_BUILT)


def update_category(conn: sqlite3.Connection, category_id: int, **fields: Any) -> dict[str, Any] | None:
    """Rename a category or change its kind. Returns None if it doesn't exist."""
    raise NotImplementedError(_NOT_BUILT)


def delete_category(conn: sqlite3.Connection, category_id: int) -> bool:
    """Delete a category. Returns True if a row was removed.

    Transactions in that category are not deleted — the foreign key is
    ON DELETE SET NULL, so they become uncategorised.
    """
    raise NotImplementedError(_NOT_BUILT)
