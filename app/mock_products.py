import requests

# Initialize the empty list
mock_products = []

def get_mock_data(category="snacks", limit=5):
    #modify the mock products list from inside this function
    global mock_products
    
    url = f"https://world.openfoodfacts.net/category/{category}.json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Populate the global list
            mock_products = [
                {
                    "count": 0,
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


#Trigger the one-time fetch immediately on load
get_mock_data()