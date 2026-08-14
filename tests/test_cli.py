import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from unittest.mock import patch, Mock

from cli import (
    view_inventory,
    delete_item,
    add_item,
    update_item,
    find_product_api,
    add_product_from_api
)


@patch("cli.requests.get")
def test_view_inventory(mock_get):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Nutella",
            "price": 450,
            "stock": 20
        }
    ]

    mock_get.return_value = mock_response

    view_inventory()

    mock_get.assert_called_once_with(
        "http://127.0.0.1:5000/inventory"
    )


@patch("builtins.input", return_value="1")
@patch("cli.requests.delete")
def test_delete_item(mock_delete, mock_input):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Item deleted successfully"
    }

    mock_delete.return_value = mock_response

    delete_item()

    mock_delete.assert_called_once_with(
        "http://127.0.0.1:5000/inventory/1"
    )


@patch(
    "builtins.input",
    side_effect=[
        "Test Juice",
        "Test Brand",
        "123456789",
        "150",
        "10"
    ]
)
@patch("cli.requests.post")
def test_add_item(mock_post, mock_input):
    mock_response = Mock()

    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 3,
        "product_name": "Test Juice",
        "brand": "Test Brand",
        "barcode": "123456789",
        "price": 150.0,
        "stock": 10
    }

    mock_post.return_value = mock_response

    add_item()

    mock_post.assert_called_once_with(
        "http://127.0.0.1:5000/inventory",
        json={
            "product_name": "Test Juice",
            "brand": "Test Brand",
            "barcode": "123456789",
            "price": 150.0,
            "stock": 10
        }
    )


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "price",
        "500"
    ]
)
@patch("cli.requests.patch")
def test_update_item(mock_patch, mock_input):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Nutella",
        "price": 500.0,
        "stock": 20
    }

    mock_patch.return_value = mock_response

    update_item()

    mock_patch.assert_called_once_with(
        "http://127.0.0.1:5000/inventory/1",
        json={
            "price": 500.0
        }
    )


@patch(
    "builtins.input",
    return_value="3017620422003"
)
@patch("cli.requests.get")
def test_find_product_api(mock_get, mock_input):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.json.return_value = {
        "barcode": "3017620422003",
        "product_name": "Nutella",
        "brand": "Ferrero",
        "ingredients": "Sugar, palm oil, hazelnuts"
    }

    mock_get.return_value = mock_response

    find_product_api()

    mock_get.assert_called_once_with(
        "http://127.0.0.1:5000/products/barcode/3017620422003"
    )


@patch(
    "builtins.input",
    side_effect=[
        "3017620422003",
        "650",
        "25"
    ]
)
@patch("cli.requests.post")
def test_add_product_from_api(mock_post, mock_input):
    mock_response = Mock()

    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 3,
        "barcode": "3017620422003",
        "product_name": "Nutella",
        "brand": "Ferrero",
        "price": 650.0,
        "stock": 25
    }

    mock_post.return_value = mock_response

    add_product_from_api()

    mock_post.assert_called_once_with(
        "http://127.0.0.1:5000/inventory/from-api/3017620422003",
        json={
            "price": 650.0,
            "stock": 25
        }
    )