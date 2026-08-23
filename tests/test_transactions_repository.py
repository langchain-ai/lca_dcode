import pytest

from ledger.repositories import transactions as repo


def make(conn, **overrides):
    fields = {
        "occurred_on": "2026-07-01",
        "description": "Coffee",
        "amount_cents": -435,
    }
    fields.update(overrides)
    return repo.create_transaction(conn, **fields)


def test_create_returns_the_stored_row(conn):
    created = make(conn)
    assert created["id"] > 0
    assert created["description"] == "Coffee"
    assert created["amount_cents"] == -435
    assert created["category_name"] is None


def test_get_returns_none_when_missing(conn):
    assert repo.get_transaction(conn, 404) is None


def test_list_is_newest_first(conn):
    make(conn, occurred_on="2026-07-01", description="older")
    make(conn, occurred_on="2026-07-09", description="newer")

    listed = repo.list_transactions(conn)

    assert [row["description"] for row in listed] == ["newer", "older"]


def test_list_respects_limit_and_offset(conn):
    for day in range(1, 6):
        make(conn, occurred_on=f"2026-07-0{day}", description=f"day {day}")

    page = repo.list_transactions(conn, limit=2, offset=1)

    assert [row["description"] for row in page] == ["day 4", "day 3"]


def test_list_includes_the_category_name(conn, sample_categories):
    make(conn, category_id=sample_categories["Groceries"])

    assert repo.list_transactions(conn)[0]["category_name"] == "Groceries"


def test_update_changes_only_the_given_columns(conn):
    created = make(conn, note="original")

    updated = repo.update_transaction(conn, created["id"], description="Tea")

    assert updated["description"] == "Tea"
    assert updated["note"] == "original"
    assert updated["amount_cents"] == -435


def test_update_rejects_unknown_columns(conn):
    created = make(conn)

    with pytest.raises(ValueError, match="unknown transaction columns"):
        repo.update_transaction(conn, created["id"], colour="blue")


def test_update_returns_none_when_missing(conn):
    assert repo.update_transaction(conn, 404, description="nope") is None


def test_delete_reports_whether_a_row_went_away(conn):
    created = make(conn)

    assert repo.delete_transaction(conn, created["id"]) is True
    assert repo.delete_transaction(conn, created["id"]) is False


def test_deleting_a_category_leaves_transactions_uncategorised(conn, sample_categories):
    created = make(conn, category_id=sample_categories["Groceries"])

    conn.execute("DELETE FROM categories WHERE id = ?", (sample_categories["Groceries"],))
    conn.commit()

    assert repo.get_transaction(conn, created["id"])["category_id"] is None


def test_totals(conn):
    make(conn, amount_cents=-435)
    make(conn, amount_cents=215_000)

    assert repo.total_cents(conn) == 214_565
    assert repo.count_transactions(conn) == 2


def test_total_of_an_empty_ledger_is_zero(conn):
    assert repo.total_cents(conn) == 0
