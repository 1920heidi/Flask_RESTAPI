import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import pytest

from app import app
from inventory_data import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_single_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    data = response.get_json()

    assert data["id"] == 1


def test_get_missing_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"


def test_add_item(client):
    new_product = {
        "barcode": "555555555",
        "product_name": "Test Juice",
        "brand": "Test Brand",
        "price": 150,
        "stock": 10
    }

    response = client.post(
        "/inventory",
        json=new_product
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["product_name"] == "Test Juice"
    assert data["price"] == 150
    assert data["stock"] == 10


def test_update_item(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 500,
            "stock": 30
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 500
    assert data["stock"] == 30


def test_delete_item(client):
    new_item = {
        "id": 999,
        "barcode": "999999",
        "product_name": "Delete Me",
        "brand": "Test",
        "price": 100,
        "stock": 1
    }

    inventory.append(new_item)

    response = client.delete("/inventory/999")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Item deleted successfully"