"""Shared wiring: the template environment and the per-request DB connection.

Routers import from here rather than from main.py, so there's no import cycle
between the app factory and the routers it registers.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from pathlib import Path

from fastapi.templating import Jinja2Templates

from ledger import db
from ledger.config import get_settings
from ledger.money import format_cents

PACKAGE_DIR = Path(__file__).parent

templates = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))
templates.env.filters["money"] = format_cents


def get_conn() -> Iterator[sqlite3.Connection]:
    """Open a connection for one request and close it afterwards.

    Use it as `conn: sqlite3.Connection = Depends(get_conn)` in every route
    that touches the database.
    """
    conn = db.connect(get_settings().database_path)
    try:
        yield conn
    finally:
        conn.close()
