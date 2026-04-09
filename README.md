# 📦 REST API Inventory Manager

A full-stack inventory management system built with **Flask** (backend REST API) and a **Python CLI** client. Products are sourced from the [OpenFoodFacts API](https://world.openfoodfacts.net/) and managed locally via a RESTful interface.

---

## 🗂️ Project Structure

```
REST-API-Inventory-Manager-Summative-Lab/
├── app/
│   ├── __init__.py
│   ├── routes.py          # Flask REST API routes
│   └── mock_products.py   # Product data & OpenFoodFacts integration
├── CLI/
│   ├── client.py          # CLI entry point (argparse)
│   └── handlers.py        # CLI command handler functions
├── server.py              # Flask app runner
├── Pipfile
├── Pipfile.lock
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pipenv

**Install pipenv if you don't have it:**
```bash
pip install pipenv
```

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd REST-API-Inventory-Manager-Summative-Lab
   ```

2. **Install dependencies and create the virtual environment**

   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**

   ```bash
   pipenv shell
   ```

---

## ▶️ Running the Application

### 1. Start the Flask Server

```bash
python server.py
```

The server will start at `http://127.0.0.1:5000`.  
On startup, it automatically fetches 5 snack products from OpenFoodFacts to populate the inventory. If a barcode is requested later and is not already in inventory, the backend also performs a live OpenFoodFacts lookup and adds that product to the in-memory inventory.

### 2. Use the CLI Client

Open a **second terminal**, activate the virtual environment, navigate to the `CLI/` directory, and run commands:

```bash
pipenv shell
cd CLI
python client.py <command> [arguments]
```

---

## 🌐 API Endpoints

| Method   | Endpoint                              | Description                        |
|----------|---------------------------------------|------------------------------------|
| `GET`    | `/`                                   | Health check / welcome message     |
| `GET`    | `/inventory`                          | List all inventory items           |
| `GET`    | `/inventory/<id>`                     | Get a single product by ID         |
| `POST`   | `/inventory/add`                      | Add a new product manually         |
| `PATCH`  | `/inventory/update/<id>/<qty>`        | Update stock quantity for a product|
| `DELETE` | `/inventory/delete/<id>`              | Delete a product by ID             |

### Example Requests

**List all products**
```bash
curl http://127.0.0.1:5000/inventory
```

**Add a new product**
```bash
curl -X POST http://127.0.0.1:5000/inventory/add \
  -H "Content-Type: application/json" \
  -d '{"name": "Granola Bar"}'
```

**Restock a product**
```bash
curl -X PATCH http://127.0.0.1:5000/inventory/update/1/10
```

**Delete a product**
```bash
curl -X DELETE http://127.0.0.1:5000/inventory/delete/1
```

---

## 💻 CLI Commands

Run all commands from the `CLI/` directory with `python client.py`.

| Command                                       | Description                              |
|-----------------------------------------------|------------------------------------------|
| `python client.py view-products`              | Display the full inventory table         |
| `python client.py add-product <name>`         | Add a new product by name                |
| `python client.py restock-product <id> <qty>` | Increase stock for a product by ID       |
| `python client.py fetch-product <barcode>`    | Fetch a product by barcode from OpenFoodFacts through the backend and add it to inventory if found |
| `python client.py delete-product <id>`        | Remove a product from inventory          |

### CLI Examples

```bash
# View all inventory
python client.py view-products

# Add a new product
python client.py add-product "Chocolate Biscuits"

# Restock product with ID 3 by 20 units
python client.py restock-product 3 20

# Fetch a product by its OpenFoodFacts barcode
python client.py fetch-product 737628064502

# Delete product with ID 2
python client.py delete-product 2
```

---

## 🔧 How It Works

### Backend (`app/`)

- **`mock_products.py`** — On import, calls `get_mock_data()` which fetches 5 products from the OpenFoodFacts `snacks` category and stores them in a global `mock_products` list. It also includes `fetch_product_by_barcode()`, which performs a live OpenFoodFacts lookup for a missing barcode and appends the result to the same in-memory inventory. The `add_to_stock()` helper updates product quantities.

- **`routes.py`** — Defines all Flask REST API routes. Routes read from and write to the `mock_products` list in memory, and the single-product route can trigger a live OpenFoodFacts fetch when a requested barcode is not already stored.

### CLI (`CLI/`)

- **`client.py`** — Uses `argparse` to define subcommands and map them to handler functions. Displays a help menu when run without arguments.

- **`handlers.py`** — Each handler makes HTTP requests to the Flask backend and prints formatted results using the `tabulate` library.

---

## 📦 Dependencies

| Package     | Purpose                          |
|-------------|----------------------------------|
| `Flask`     | Web framework for the REST API   |
| `requests`  | HTTP client for CLI and API fetch|
| `tabulate`  | Table formatting in the CLI      |

Dependencies are managed via **Pipenv**. To add a new package:
```bash
pipenv install <package-name>
```

---

## ⚠️ Notes

- **Data is stored in memory only.** All inventory data resets when the Flask server restarts.
- Ensure the Flask server is running before using the CLI client.
- The OpenFoodFacts integration runs on server startup to seed inventory and can also run again when `fetch-product` requests a barcode that is not already stored.
- **Product IDs are strings across the project.** CLI commands and backend routes both treat IDs as string values (for example, OpenFoodFacts barcodes).

---

## 📝 License

This project was created as a summative lab project for educational purposes.