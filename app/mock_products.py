import requests
import json
import os

# Initialize the empty list
mock_products = []
file_path = "mock_products_store.json"

# OpenFoodFacts headers for API requests
OPEN_FOOD_FACTS_HEADERS = {
    "User-Agent": "InventoryManagerCLI/1.0 (student-project)",
    "Accept": "application/json",
}


def persist_products():
    """Save the current list to disk so it survives server restarts."""
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(mock_products, f, indent=2)


def load_products_from_disk():
    """Load saved list from disk. Returns True if loading worked."""
    global mock_products
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        if isinstance(loaded, list):
            # Replace the list with saved data from disk.
            mock_products = loaded
            return True
    except Exception as e:
        print(f"Failed to load persisted data: {e}")

    return False


def get_mock_data(category="snacks", limit=5):
    # modify the mock products list from inside this function
    global mock_products

    url = f"https://world.openfoodfacts.net/category/{category}.json"

    try:
        response = requests.get(url, headers=OPEN_FOOD_FACTS_HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Populate the global list
            mock_products = [
                {
                    "count": 1,
                    "id": p.get("code"),
                    "name": p.get("product_name", "Unknown"),
                    "brand": p.get("brands", "Generic"),
                    "nutriscore": p.get("nutriscore_grade", "unknown"),
                    "image": p.get("image_front_small_url")
                }
                for p in data.get("products", [])[:limit]
            ]
            persist_products()
    except Exception as e:
        print(f"Failed to fetch mock data: {e}")


def add_to_stock(product_id, quantity):
    global mock_products
    for p in mock_products:
        if p['id'] == product_id:
            p['count'] += int(quantity)
            persist_products()
            return p
    return None


def add_new_product(name):
    new_p_id = max((int(p['id']) for p in mock_products if str(p['id']).isdigit()), default=0) + 1
    new_product = {
        "id": f"{new_p_id}",
        "name": name.strip(),
        "count": 1,
    }
    mock_products.append(new_product)
    persist_products()
    return new_product


def delete_product_by_id(product_id):
    for idx, product in enumerate(mock_products):
        if product.get("id") == product_id:
            del mock_products[idx]
            persist_products()
            return True
    return False


def fetch_product_by_barcode(barcode):
    global mock_products

    existing_product = next((product for product in mock_products if product['id'] == barcode), None)
    if existing_product:
        return existing_product

    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}.json"

    try:
        response = requests.get(url, headers=OPEN_FOOD_FACTS_HEADERS, timeout=10)
        if response.status_code != 200:
            return None

        data = response.json()
        product = data.get("product")
        if not product:
            return None

        fetched_product = {
            "count": 1,
            "id": barcode,
            "name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", "Generic"),
            "nutriscore": product.get("nutriscore_grade", "unknown"),
            "image": product.get("image_front_small_url"),
        }
        mock_products.append(fetched_product)
        persist_products()
        return fetched_product
    except Exception:
        return None


# Loads persisted data first, fallbacks to a one-time seed fetch.
if not load_products_from_disk() or not mock_products:
    get_mock_data()