from flask import Flask, jsonify, request
from inventory_data import inventory
from openfoodfacts import get_product_by_barcode
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route("/admin")
def admin_portal():
    return render_template("index.html", inventory=inventory)

@app.route("/")
def home():
    return "Inventory Management System is running!"

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):

    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["product_name", "price", "stock"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "barcode": data.get("barcode"),
        "product_name": data["product_name"],
        "brand": data.get("brand"),
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Item deleted successfully"
            }), 200

    return jsonify({"error": "Item not found"}), 404

@app.route("/products/barcode/<barcode>", methods=["GET"])
def find_product_by_barcode(barcode):

    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200

@app.route("/inventory/from-api/<barcode>", methods=["POST"])
def add_product_from_api(barcode):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "price" not in data or "stock" not in data:
        return jsonify({
            "error": "price and stock are required"
        }), 400

    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found on OpenFoodFacts"
        }), 404

    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "barcode": product["barcode"],
        "product_name": product["product_name"],
        "brand": product["brand"],
        "ingredients": product["ingredients"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201

@app.route("/admin/add", methods=["POST"])
def admin_add_item():
    product_name = request.form.get("product_name")
    brand = request.form.get("brand")
    barcode = request.form.get("barcode")
    price = request.form.get("price")
    stock = request.form.get("stock")

    if not product_name or not price or not stock:
        return "Product name, price and stock are required", 400

    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "barcode": barcode,
        "product_name": product_name,
        "brand": brand,
        "price": float(price),
        "stock": int(stock)
    }

    inventory.append(new_item)

    return render_template("index.html", inventory=inventory)

@app.route("/admin/edit/<int:item_id>", methods=["POST"])
def admin_edit_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            item["product_name"] = request.form.get("product_name")
            item["brand"] = request.form.get("brand")
            item["barcode"] = request.form.get("barcode")
            item["price"] = float(request.form.get("price"))
            item["stock"] = int(request.form.get("stock"))

            return render_template("index.html", inventory=inventory)

    return "Item not found", 404


@app.route("/admin/delete/<int:item_id>", methods=["POST"])
def admin_delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return render_template("index.html", inventory=inventory)

    return "Item not found", 404

# Search OpenFoodFacts from the admin portal
@app.route("/admin/search-api", methods=["POST"])
def admin_search_api():
    barcode = request.form.get("barcode")

    product = get_product_by_barcode(barcode)

    if product is None:
        return render_template(
            "index.html",
            inventory=inventory,
            api_error="Product not found on OpenFoodFacts"
        )

    return render_template(
        "index.html",
        inventory=inventory,
        api_product=product
    )

@app.route("/admin/add-from-api/<barcode>", methods=["POST"])
def admin_add_from_api(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return "Product not found", 404

    price = request.form.get("price")
    stock = request.form.get("stock")

    new_id = max(
        [item["id"] for item in inventory],
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "barcode": product["barcode"],
        "product_name": product["product_name"],
        "brand": product["brand"],
        "ingredients": product["ingredients"],
        "price": float(price),
        "stock": int(stock)
    }

    inventory.append(new_item)

    return render_template(
        "index.html",
        inventory=inventory
    )

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)