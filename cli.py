import requests

API_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{API_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("Inventory is empty.")
            return

        for item in items:
            print(
                f'ID: {item["id"]} | '
                f'Product: {item["product_name"]} | '
                f'Price: {item["price"]} | '
                f'Stock: {item["stock"]}'
            )
    else:
        print("Failed to fetch inventory.")


def view_item():
    item_id = input("Enter item ID: ")

    response = requests.get(
        f"{API_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print(response.json())
    else:
        print("Item not found.")


def add_item():
    product_name = input("Product name: ")
    brand = input("Brand: ")
    barcode = input("Barcode: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))

    data = {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "price": price,
        "stock": stock
    }

    response = requests.post(
        f"{API_URL}/inventory",
        json=data
    )

    if response.status_code == 201:
        print("Product added successfully.")
        print(response.json())
    else:
        print("Failed to add product.")
        print(response.json())


def update_item():
    item_id = input("Enter item ID: ")

    field = input(
        "What do you want to update? "
        "(price/stock/brand/product_name): "
    )

    value = input("Enter new value: ")

    if field == "price":
        value = float(value)

    if field == "stock":
        value = int(value)

    data = {
        field: value
    }

    response = requests.patch(
        f"{API_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("Item updated successfully.")
        print(response.json())
    else:
        print("Failed to update item.")
        print(response.json())


def delete_item():
    item_id = input("Enter item ID to delete: ")

    response = requests.delete(
        f"{API_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print("Item deleted successfully.")
    else:
        print("Failed to delete item.")
        print(response.json())


def find_product_api():
    barcode = input("Enter product barcode: ")

    response = requests.get(
        f"{API_URL}/products/barcode/{barcode}"
    )

    if response.status_code == 200:
        product = response.json()

        print("\nProduct found:")
        print(f'Name: {product["product_name"]}')
        print(f'Brand: {product["brand"]}')
        print(f'Barcode: {product["barcode"]}')
        print(f'Ingredients: {product["ingredients"]}')

    else:
        print("Product not found on OpenFoodFacts.")


def add_product_from_api():
    barcode = input("Enter product barcode: ")
    price = float(input("Enter selling price: "))
    stock = int(input("Enter stock quantity: "))

    data = {
        "price": price,
        "stock": stock
    }

    response = requests.post(
        f"{API_URL}/inventory/from-api/{barcode}",
        json=data
    )

    if response.status_code == 201:
        print("Product added from OpenFoodFacts successfully.")
        print(response.json())
    else:
        print("Failed to add product.")
        print(response.json())


def menu():
    while True:
        print("\n==============================")
        print(" INVENTORY MANAGEMENT SYSTEM")
        print("==============================")
        print("1. View all inventory")
        print("2. View one item")
        print("3. Add new item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Find product on OpenFoodFacts")
        print("7. Add product from OpenFoodFacts")
        print("8. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            find_product_api()

        elif choice == "7":
            add_product_from_api()

        elif choice == "8":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    menu()