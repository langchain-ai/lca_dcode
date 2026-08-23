"""Runtime settings.

Deliberately tiny: one env var, no framework. If this grows past a handful of
values, swap it for pydantic-settings.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    database_path: Path


def get_settings() -> Settings:
    """Read settings from the environment on every call.

    Not cached on purpose — the test suite points LEDGER_DATABASE_PATH at a
    temporary file per test.
    """
    raw = os.environ.get("LEDGER_DATABASE_PATH")
    path = Path(raw) if raw else PROJECT_ROOT / "ledger.db"
    return Settings(database_path=path)
