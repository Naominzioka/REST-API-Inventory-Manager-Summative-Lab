import requests

# Initialize the empty list
mock_products = []

# OpenFoodFacts headers for API requests
OPEN_FOOD_FACTS_HEADERS = {
    "User-Agent": "InventoryManagerCLI/1.0 (student-project)",
    "Accept": "application/json",
}

def get_mock_data(category="snacks", limit=5):
    #modify the mock products list from inside this function
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
    except Exception as e:
        print(f"Failed to fetch mock data: {e}")
        
def add_to_stock(product_id, quantity):
    global mock_products
    for p in mock_products:
        if p['id'] == product_id:
            p['count'] += int(quantity)
            return p
    return None


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
        return fetched_product
    except Exception:
        return None


#Trigger the one-time fetch immediately on load
get_mock_data()