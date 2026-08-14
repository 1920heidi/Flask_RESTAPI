import requests
from unittest.mock import patch, Mock

from openfoodfacts import get_product_by_barcode


@patch("openfoodfacts.requests.get")
def test_get_product_by_barcode_success(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar"
        }
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    product = get_product_by_barcode("123456789")

    assert product is not None
    assert product["barcode"] == "123456789"
    assert product["product_name"] == "Organic Almond Milk"
    assert product["brand"] == "Silk"
    assert product["ingredients"] == "Filtered water, almonds, cane sugar"


@patch("openfoodfacts.requests.get")
def test_get_product_by_barcode_not_found(mock_get):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0
    }

    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    product = get_product_by_barcode("000000000")

    assert product is None


@patch("openfoodfacts.requests.get")
def test_get_product_by_barcode_api_failure(mock_get):
    mock_get.side_effect = requests.RequestException("API unavailable")

    product = get_product_by_barcode("123456789")

    assert product is None