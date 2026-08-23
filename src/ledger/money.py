"""Money helpers.

Every amount in this codebase is an integer number of cents. Negative means
money out, positive means money in. See .deepagents/AGENTS.md.
"""

from __future__ import annotations


def parse_amount_to_cents(text: str) -> int:
    """Turn a user-typed amount like "12.50" or "-8.15" into cents."""
    cleaned = text.strip().replace("$", "").replace(",", "")
    if not cleaned:
        raise ValueError("amount is required")
    return int(float(cleaned) * 100)


def format_cents(cents: int) -> str:
    """Render cents for display: 1250 -> "$12.50", -815 -> "-$8.15"."""
    sign = "-" if cents < 0 else ""
    whole, part = divmod(abs(cents), 100)
    return f"{sign}${whole:,}.{part:02d}"
