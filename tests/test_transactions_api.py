"""Router tests for transactions — the reference example for testing a resource."""


def test_dashboard_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Ledger" in response.text


def test_transactions_page_renders(client):
    response = client.get("/transactions")
    assert response.status_code == 200


def test_create_and_read_back(client):
    created = client.post(
        "/api/transactions",
        json={"occurred_on": "2026-07-01", "description": "Coffee", "amount_cents": -435},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["description"] == "Coffee"
    assert body["amount_cents"] == -435

    fetched = client.get(f"/api/transactions/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]


def test_list_returns_created_rows(client):
    client.post(
        "/api/transactions",
        json={"occurred_on": "2026-07-01", "description": "Coffee", "amount_cents": -435},
    )

    response = client.get("/api/transactions")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_blank_description_is_rejected(client):
    response = client.post(
        "/api/transactions",
        json={"occurred_on": "2026-07-01", "description": "   ", "amount_cents": -435},
    )
    assert response.status_code == 422


def test_bad_date_is_rejected(client):
    response = client.post(
        "/api/transactions",
        json={"occurred_on": "last tuesday", "description": "Coffee", "amount_cents": -435},
    )
    assert response.status_code == 422


def test_patch_updates_one_field(client):
    created = client.post(
        "/api/transactions",
        json={"occurred_on": "2026-07-01", "description": "Coffee", "amount_cents": -435},
    ).json()

    response = client.patch(f"/api/transactions/{created['id']}", json={"description": "Tea"})

    assert response.status_code == 200
    assert response.json()["description"] == "Tea"
    assert response.json()["amount_cents"] == -435


def test_delete_then_404(client):
    created = client.post(
        "/api/transactions",
        json={"occurred_on": "2026-07-01", "description": "Coffee", "amount_cents": -435},
    ).json()

    assert client.delete(f"/api/transactions/{created['id']}").status_code == 204
    assert client.get(f"/api/transactions/{created['id']}").status_code == 404


def test_missing_transaction_is_404(client):
    assert client.get("/api/transactions/404").status_code == 404


def test_html_form_creates_a_transaction(client):
    response = client.post(
        "/transactions",
        data={"occurred_on": "2026-07-01", "description": "Coffee", "amount": "-4.35"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert client.get("/api/transactions").json()[0]["description"] == "Coffee"
