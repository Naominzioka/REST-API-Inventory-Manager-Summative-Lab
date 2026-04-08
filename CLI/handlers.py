from tabulate import tabulate
import requests

#configuration
BASE_URL = "http://127.0.0.1:5000"
#headers for all requests to the backend
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "InventoryManagerCLI/1.0",
}

#view inventory details
def view_products(cli_context, args):
    try:
        response = requests.get(f"{BASE_URL}/inventory", headers=DEFAULT_HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(tabulate(data, headers="keys", tablefmt="grid"))
        else:
            print("Error: Could not retrieve inventory.")
    except Exception as e:
        print(f"Connection Error: {e}")

#add new product
def add_product(cli_context, args):
    try:
        payload = {
            "name": args.name
        }
        response = requests.post(
            f"{BASE_URL}/inventory/add",
            json=payload,
            headers={**DEFAULT_HEADERS, "Content-Type": "application/json"}
            )
        if response.status_code == 201:
            print(f"New product '{args.name}' added successfully. ")
            data = response.json()
            view_products(cli_context, args)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the backend. Is your Flask server running?")


def restock_product(cli_context, args):
    try:
        url = f"{BASE_URL}/inventory/update/{args.product_id}/{args.quantity}"
        response = requests.patch(url, headers=DEFAULT_HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['message']}") 
            print(f"Product: {data['product']} restocked.")
            print(f"New total is {data['new_total']}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend.")


#delete product
def delete_product(cli_context, args):
    try:
        url = f'{BASE_URL}/inventory/delete/{args.product_id}'
        response = requests.delete(url, headers=DEFAULT_HEADERS)
        if response.status_code == 204:
            print(f"Successfully deleted product {args.product_id}")
            view_products(cli_context, args)
        elif response.status_code == 404:
            print(f"Error: Product ID {args.product_id} not found.")
        else:
            print(f"Failed to delete. Server returned: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend.Run your flask server")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#find item on api
def fetch_product(cli_context, args):
    """Hits the Flask backend to trigger an OpenFoodFacts API fetch."""
    print(f"\n📡 Requesting backend to fetch barcode: {args.barcode}...")
    
    try:
        url = f"{BASE_URL}/inventory/{args.barcode}"
        response = requests.get(url, headers=DEFAULT_HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['name']} | Stock {data['count']}")
        elif response.status_code == 404:
            print(f"❌ Error: Product {args.barcode} not found on OpenFoodFacts.")
        else:
            print(f"⚠️  Backend returned error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the backend. Is your Flask server running?")