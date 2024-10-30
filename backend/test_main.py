from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_get_accounts():
    response = client.get("/accounts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_account():
    account_data = {
        "name": "Test Account",
        "balance": 1000.0,
        "currency": "USD",
        "type": "savings",
    }
    response = client.post("/accounts/", json=account_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == account_data["name"]
    assert response_data["balance"] == account_data["balance"]
    assert response_data["currency"] == account_data["currency"]
    assert response_data["type"] == account_data["type"]


def test_get_accounts_with_data():
    # Create multiple accounts
    account_data_1 = {
        "name": "Account 1",
        "balance": 500.0,
        "currency": "USD",
        "type": "checking",
    }
    account_data_2 = {
        "name": "Account 2",
        "balance": 1500.0,
        "currency": "EUR",
        "type": "savings",
    }
    client.post("/accounts/", json=account_data_1)
    client.post("/accounts/", json=account_data_2)

    response = client.get("/accounts/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]["name"] == account_data_1["name"]
    assert response_data[1]["name"] == account_data_2["name"]
