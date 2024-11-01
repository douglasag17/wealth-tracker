from fastapi.testclient import TestClient

from .database import create_db_and_tables, drop_db_and_tables
from .main import app

client = TestClient(app)
drop_db_and_tables()
create_db_and_tables()


# Currencies endpoints
def test_create_currency():
    response = client.post("/currencies/", json={"name": "EUR"})
    assert response.status_code == 200
    assert response.json()["name"] == "EUR"


def test_get_currencies():
    response = client.get("/currencies/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "EUR"


def test_get_currency():
    response = client.get("/currencies/1")
    assert response.status_code == 200
    assert response.json()["name"] == "EUR"


def test_update_currency():
    response = client.patch("/currencies/1", json={"name": "USD"})
    assert response.status_code == 200
    assert response.json()["name"] == "USD"


def test_delete_currency():
    response = client.delete("/currencies/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Account Types endpoints
def test_create_account_type():
    response = client.post("/account_types/", json={"type": "checking account"})
    assert response.status_code == 200
    assert response.json()["type"] == "checking account"


def test_get_account_types():
    response = client.get("/account_types/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["type"] == "checking account"


def test_get_account_type():
    response = client.get("/account_types/1")
    assert response.status_code == 200
    assert response.json()["type"] == "checking account"


def test_update_account_type():
    response = client.patch("/account_types/1", json={"type": "savings account"})
    assert response.status_code == 200
    assert response.json()["type"] == "savings account"


def test_delete_account_type():
    response = client.delete("/account_types/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Accounts endpoints
def test_create_account():
    response = client.post(
        "/accounts/",
        json={
            "name": "bancolombia savings account",
            "account_type_id": 1,
            "currency_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "bancolombia savings account"


def test_get_accounts():
    response = client.get("/accounts/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "bancolombia savings account"


def test_get_account():
    response = client.get("/accounts/1")
    assert response.status_code == 200
    assert response.json()["name"] == "bancolombia savings account"


def test_update_account():
    response = client.patch(
        "/accounts/1", json={"name": "bancolombia savings account 2"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "bancolombia savings account 2"


def test_delete_account():
    response = client.delete("/accounts/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Categories endpoints
def test_create_category():
    response = client.post(
        "/categories/", json={"name": "groceries", "type": "expense"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "groceries"


def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "groceries"


def test_get_category():
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json()["name"] == "groceries"


def test_update_category():
    response = client.patch("/categories/1", json={"name": "groceries 2"})
    assert response.status_code == 200
    assert response.json()["name"] == "groceries 2"


def test_delete_category():
    response = client.delete("/categories/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Subcategories endpoints
def test_create_subcategory():
    response = client.post(
        "/sub_categories/",
        json={"name": "restaurant", "type_expense": "wants", "category_id": 1},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "restaurant"


def test_get_sub_categories():
    response = client.get("/sub_categories/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "restaurant"


def test_get_subcategory():
    response = client.get("/sub_categories/1")
    assert response.status_code == 200
    assert response.json()["name"] == "restaurant"


def test_update_subcategory():
    response = client.patch("/sub_categories/1", json={"name": "restaurant 2"})
    assert response.status_code == 200
    assert response.json()["name"] == "restaurant 2"


def test_delete_subcategory():
    response = client.delete("/sub_categories/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Transactions endpoints
def test_create_transaction():
    response = client.post(
        "/transactions/",
        json={
            "amount": 100.55,
            "transaction_date": "2024-10-02 12:30:00",
            "description": "restaurant bill",
            "account_id": 1,
            "category_id": 1,
            "subcategory_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["amount"] == "100.55"


def test_get_transactions():
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["amount"] == "100.55"
    assert response.json()[0]["description"] == "restaurant bill"


def test_get_transaction():
    response = client.get("/transactions/1")
    assert response.status_code == 200
    assert response.json()["amount"] == "100.55"
    assert response.json()["description"] == "restaurant bill"


def test_update_transaction():
    response = client.patch("/transactions/1", json={"amount": 200.33})
    assert response.status_code == 200
    assert response.json()["amount"] == "200.33"


def test_delete_transaction():
    response = client.delete("/transactions/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Planned Transactions endpoints
def test_create_planned_transaction():
    response = client.post(
        "/planned_transactions/",
        json={
            "amount": 100.55,
            "transaction_date": "2024-10-02 12:30:00",
            "description": "restaurant bill",
            "account_id": 1,
            "category_id": 1,
            "subcategory_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["amount"] == "100.55"


def test_get_planned_transactions():
    response = client.get("/planned_transactions/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["amount"] == "100.55"
    assert response.json()[0]["description"] == "restaurant bill"


def test_get_planned_transaction():
    response = client.get("/planned_transactions/1")
    assert response.status_code == 200
    assert response.json()["amount"] == "100.55"
    assert response.json()["description"] == "restaurant bill"


def test_update_planned_transaction():
    response = client.patch("/planned_transactions/1", json={"amount": 200.33})
    assert response.status_code == 200
    assert response.json()["amount"] == "200.33"


def test_delete_planned_transaction():
    response = client.delete("/planned_transactions/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Budgets endpoints
def test_create_budget():
    response = client.post(
        "/budgets/",
        json={"year": 2024, "month": 10, "budget": 1000.00, "subcategory_id": 1},
    )
    assert response.status_code == 200
    assert response.json()["budget"] == "1000.00"


def test_get_budgets():
    response = client.get("/budgets/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["budget"] == "1000.00"


def test_get_budget():
    response = client.get("/budgets/1")
    assert response.status_code == 200
    assert response.json()["budget"] == "1000.00"


def test_update_budget():
    response = client.patch("/budgets/1", json={"budget": 2000.00})
    assert response.status_code == 200
    assert response.json()["budget"] == "2000.00"


def test_delete_budget():
    response = client.delete("/budgets/1")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


# Endpoints with precalculated data
def populate_db():
    create_db_and_tables()

    # Create some mock currencies
    client.post("/currencies/", json={"name": "COP"})

    # Create some mock account types
    client.post("/account_types/", json={"type": "savings account"})
    client.post("/account_types/", json={"type": "credit card"})

    # Create some mock accounts
    client.post(
        "/accounts/",
        json={
            "name": "bancolombia savings account",
            "account_type_id": 1,
            "currency_id": 1,
        },
    )
    client.post(
        "/accounts/",
        json={
            "name": "bancolombia mastercard black",
            "account_type_id": 2,
            "currency_id": 1,
        },
    )

    # Create some mock categories
    client.post("/categories/", json={"name": "food", "type": "expense"})
    client.post("/categories/", json={"name": "income", "type": "income"})

    # Create some mock subcategories
    client.post(
        "/sub_categories/",
        json={"name": "restaurant", "type_expense": "wants", "category_id": 1},
    )
    client.post(
        "/sub_categories/",
        json={"name": "groceries", "type_expense": "needs", "category_id": 1},
    )
    client.post(
        "/sub_categories/",
        json={"name": "wage", "category_id": 2},
    )

    # Create some mock transactions
    client.post(
        "/transactions/",
        json={
            "amount": 100.55,
            "transaction_date": "2024-10-02 12:30:00",
            "description": "restaurant bill",
            "account_id": 1,
            "category_id": 1,
            "subcategory_id": 1,
        },
    )
    client.post(
        "/transactions/",
        json={
            "amount": 200,
            "transaction_date": "2024-10-15 12:30:00",
            "description": "groceries",
            "account_id": 2,
            "category_id": 1,
            "subcategory_id": 2,
        },
    )
    client.post(
        "/transactions/",
        json={
            "amount": 700,
            "transaction_date": "2024-10-25 12:30:00",
            "description": "wage",
            "account_id": 1,
            "category_id": 2,
            "subcategory_id": 2,
        },
    )


def test_get_total_balance():
    populate_db()
    response = client.get("/total_balance/")
    assert response.status_code == 200
    assert response.json() == {"total_balance": 399.45}
    drop_db_and_tables()


def test_get_total_account_balance():
    populate_db()
    response = client.get("/total_balance/1/")
    assert response.status_code == 200
    assert response.json() == {"total_balance": 599.45}
    drop_db_and_tables()


def test_get_total_balance_per_account():
    populate_db()
    response = client.get("/total_balance_per_account/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "bancolombia savings account",
            "account_type": "savings account",
            "total_balance": 599.45,
            "currency": "COP",
        },
        {
            "id": 2,
            "name": "bancolombia mastercard black",
            "account_type": "credit card",
            "total_balance": -200.00,
            "currency": "COP",
        },
    ]
    drop_db_and_tables()
