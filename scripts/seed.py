"""Fill the database with plausible sample data.

Deterministic (fixed random seed) so everyone in the course sees the same
numbers. Safe to re-run: it clears both tables first.

    make seed
"""

from __future__ import annotations

import random
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ledger import db  # noqa: E402
from ledger.config import get_settings  # noqa: E402

RANDOM_SEED = 20260817
MONTHS_OF_HISTORY = 8

CATEGORIES: list[tuple[str, str]] = [
    ("Salary", "income"),
    ("Freelance", "income"),
    ("Rent", "expense"),
    ("Groceries", "expense"),
    ("Restaurants", "expense"),
    ("Transit", "expense"),
    ("Utilities", "expense"),
    ("Health", "expense"),
    ("Subscriptions", "expense"),
    ("Travel", "expense"),
    ("Home", "expense"),
    ("Gifts", "expense"),
]

# category -> (merchant options, cent range, roughly how many per month)
EXPENSE_PATTERNS: dict[str, tuple[list[str], tuple[int, int], int]] = {
    "Groceries": (["Berkeley Bowl", "Trader Joe's", "Safeway", "Corner Market"], (1800, 14200), 7),
    "Restaurants": (["Sunrise Diner", "Pho 88", "Taqueria Cinco", "Blue Bottle"], (650, 6800), 6),
    "Transit": (["Clipper reload", "BART fare", "Gas — Shell", "Parking meter"], (275, 6500), 4),
    "Utilities": (["PG&E", "City Water", "Comcast"], (3200, 18900), 3),
    "Health": (["Walgreens", "Dr. Okafor copay", "Dental cleaning"], (1500, 22000), 1),
    "Subscriptions": (["Spotify", "Backblaze", "Domain renewal", "Gym"], (599, 4500), 3),
    "Travel": (["Alaska Airlines", "Airbnb — Bend", "Amtrak"], (7800, 48000), 1),
    "Home": (["Ace Hardware", "IKEA", "Cleaning service"], (2200, 26000), 2),
    "Gifts": (["Bookshop", "Flowers", "Birthday dinner"], (2000, 12000), 1),
}


def month_starts(count: int, *, today: date) -> list[date]:
    """The first day of each of the last `count` months, oldest first."""
    starts = []
    year, month = today.year, today.month
    for _ in range(count):
        starts.append(date(year, month, 1))
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    return list(reversed(starts))


def build_rows(today: date) -> list[tuple[str, str, int, str, str | None]]:
    """Return (occurred_on, description, amount_cents, category_name, note)."""
    rng = random.Random(RANDOM_SEED)
    rows: list[tuple[str, str, int, str, str | None]] = []

    for start in month_starts(MONTHS_OF_HISTORY, today=today):
        # Income
        rows.append((start.replace(day=1).isoformat(), "Paycheck", 215_000, "Salary", None))
        mid = start + timedelta(days=14)
        rows.append((mid.isoformat(), "Paycheck", 215_000, "Salary", None))
        if rng.random() < 0.4:
            day = start + timedelta(days=rng.randint(2, 25))
            rows.append(
                (day.isoformat(), "Invoice — Hollis & Co", rng.randrange(40_000, 180_000), "Freelance", None)
            )

        # Rent
        rows.append((start.isoformat(), "Rent — 14th St", -232_500, "Rent", None))

        # Everything else
        for category, (merchants, (low, high), per_month) in EXPENSE_PATTERNS.items():
            for _ in range(rng.randint(max(0, per_month - 2), per_month + 1)):
                day = start + timedelta(days=rng.randint(0, 27))
                if day > today:
                    continue
                note = "reimbursable" if category == "Travel" and rng.random() < 0.3 else None
                rows.append(
                    (day.isoformat(), rng.choice(merchants), -rng.randrange(low, high), category, note)
                )

    rows.sort(key=lambda row: row[0])
    return rows


def main() -> int:
    settings = get_settings()
    conn = db.connect(settings.database_path)
    try:
        db.migrate(conn)

        conn.execute("DELETE FROM transactions")
        conn.execute("DELETE FROM categories")
        conn.executemany("INSERT INTO categories (name, kind) VALUES (?, ?)", CATEGORIES)

        ids = {row["name"]: row["id"] for row in conn.execute("SELECT id, name FROM categories")}

        rows = build_rows(date.today())
        conn.executemany(
            """
            INSERT INTO transactions (occurred_on, description, amount_cents, category_id, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            [(d, desc, cents, ids[cat], note) for d, desc, cents, cat, note in rows],
        )
        conn.commit()

        total = conn.execute("SELECT COALESCE(SUM(amount_cents), 0) AS t FROM transactions").fetchone()["t"]
        print(f"Seeded {len(rows)} transactions across {len(CATEGORIES)} categories.")
        print(f"Database: {settings.database_path}")
        print(f"Net total: {total / 100:,.2f}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
