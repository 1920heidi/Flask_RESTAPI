# Inventory Management System

A Flask-based inventory management system that allows users to create,
view, update, and delete inventory products.

The application also integrates with the OpenFoodFacts API to retrieve
real-world product information using product barcodes.

## Features

- View all inventory products
- View individual products
- Add inventory products
- Update inventory products
- Delete inventory products
- Search OpenFoodFacts using a barcode
- Add OpenFoodFacts products to inventory
- Browser-based administrator portal
- Command-line interface (CLI)
- Automated testing with pytest

## Technologies Used

- Python
- Flask
- Requests
- Pytest
- HTML
- OpenFoodFacts API

## Project Structure

inventory_management_system/
├── app.py
├── cli.py
├── inventory_data.py
├── openfoodfacts.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── tests/
    ├── test_inventory_api.py
    ├── test_openfoodfacts.py
    └── test_cli.py

## Installation

Clone the repository:

git clone <repository-url>

Navigate into the project:

cd inventory_management_system

Create a virtual environment:

python3 -m venv venv

Activate the virtual environment on macOS/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Running the Application

Run:

python app.py

Then visit:

http://127.0.0.1:5000/admin

## REST API Endpoints

GET /inventory
Returns all inventory products.

GET /inventory/<id>
Returns one inventory product.

POST /inventory
Creates a new inventory product.

PATCH /inventory/<id>
Updates an existing inventory product.

DELETE /inventory/<id>
Deletes an inventory product.

GET /products/barcode/<barcode>
Retrieves product information from OpenFoodFacts.

POST /inventory/from-api/<barcode>
Retrieves a product from OpenFoodFacts and adds it to inventory.

## CLI

Keep the Flask application running in one terminal.

Open another terminal and run:

python cli.py

The CLI provides options for viewing, adding, updating and deleting
inventory products and searching OpenFoodFacts.

## Testing

Run:

python -m pytest

The test suite covers:

- Flask REST API endpoints
- CRUD functionality
- OpenFoodFacts API interactions
- CLI functionality

External API requests are mocked during testing using unittest.mock.

## Data Storage

This project uses a Python list as temporary simulated storage as required
by the assignment. Data is therefore reset when the application process
restarts.

## External API

Product information is retrieved from the OpenFoodFacts API using product
barcodes.