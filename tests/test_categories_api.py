"""Specs for category management.

These are skipped because the feature doesn't exist yet. Remove the skip marks
as you build it — they're your definition of done.

This is the only feature in the course that ships with tests. For everything
after it, writing them is part of the work.
"""

import pytest

pytestmark = pytest.mark.skip(reason="Category management is not built yet")


def test_categories_page_lists_categories(client):
    client.post("/api/categories", json={"name": "Groceries", "kind": "expense"})

    response = client.get("/categories")

    assert response.status_code == 200
    assert "Groceries" in response.text


def test_create_category(client):
    response = client.post("/api/categories", json={"name": "Groceries", "kind": "expense"})

    assert response.status_code == 201
    assert response.json()["name"] == "Groceries"
    assert response.json()["kind"] == "expense"


def test_duplicate_name_is_a_conflict(client):
    client.post("/api/categories", json={"name": "Groceries", "kind": "expense"})

    response = client.post("/api/categories", json={"name": "Groceries", "kind": "expense"})

    assert response.status_code == 409


def test_invalid_kind_is_rejected(client):
    response = client.post("/api/categories", json={"name": "Groceries", "kind": "sideways"})

    assert response.status_code == 422


def test_rename_a_category(client):
    created = client.post("/api/categories", json={"name": "Food", "kind": "expense"}).json()

    response = client.patch(f"/api/categories/{created['id']}", json={"name": "Groceries"})

    assert response.status_code == 200
    assert response.json()["name"] == "Groceries"


def test_deleting_a_category_uncategorises_its_transactions(client):
    category = client.post("/api/categories", json={"name": "Groceries", "kind": "expense"}).json()
    transaction = client.post(
        "/api/transactions",
        json={
            "occurred_on": "2026-07-01",
            "description": "Berkeley Bowl",
            "amount_cents": -7422,
            "category_id": category["id"],
        },
    ).json()

    assert client.delete(f"/api/categories/{category['id']}").status_code == 204

    remaining = client.get(f"/api/transactions/{transaction['id']}").json()
    assert remaining["category_id"] is None


def test_transactions_can_be_filed_under_a_category(client):
    category = client.post("/api/categories", json={"name": "Groceries", "kind": "expense"}).json()

    created = client.post(
        "/api/transactions",
        json={
            "occurred_on": "2026-07-01",
            "description": "Berkeley Bowl",
            "amount_cents": -7422,
            "category_id": category["id"],
        },
    )

    assert created.status_code == 201
    assert created.json()["category_name"] == "Groceries"
