import requests

BASE_URL = "https://world.openfoodfacts.org"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (student-project)"
}


def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "barcode": barcode,
            "product_name": product.get("product_name"),
            "brand": product.get("brands"),
            "ingredients": product.get("ingredients_text")
        }

    except requests.RequestException:
        return None