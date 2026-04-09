from flask import Flask, jsonify, request
from app.mock_products import mock_products, add_to_stock, fetch_product_by_barcode

app = Flask(__name__)

#test to see if server is working
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Inventory Management app"})

#route for listing products
@app.route('/inventory', methods=["GET"])
def inventory():
    items = [
        {'id': p['id'], 'name': p['name'], 'count': p['count']}
        for p in mock_products
    ]
    return jsonify(items)

#route to get a particular product
@app.route('/inventory/<string:id>', methods=['GET'])
def get_inventory_id(id):
    for p in mock_products:
        if p['id'] == id:
            item = {'id': p['id'], 'name': p['name'], 'count': p['count']}
            return jsonify(item), 200

    fetched_product = fetch_product_by_barcode(id)
    if fetched_product:
        item = {
            'id': fetched_product['id'],
            'name': fetched_product['name'],
            'count': fetched_product['count'],
        }
        return jsonify(item), 200

    return jsonify({"message": "No product found"}), 404

#route to create a new entry
@app.route('/inventory/add', methods=['POST'])
def add_new_product():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Product name is required"}), 400
    
    new_p_id = max((int(p['id']) for p in mock_products if p['id'].isdigit()), default=0) + 1
    new_product = {
        "id": f"{new_p_id}",
        "name": data['name'],
        "count": 1,
    }
    mock_products.append(new_product)
    return jsonify(new_product), 201

#route to update stock of an existing product    
@app.route('/inventory/update/<string:id>/<int:qty>', methods=['PATCH'])
def update_stock(id, qty):
    added_item = add_to_stock(id, qty)
    if added_item:
        return jsonify({"message": f"Added {qty} units",
                       "product": added_item['name'],
                       "new_total": added_item['count']})
        
    return jsonify({"error": "Product not found"}), 404

#delete a product
@app.route('/inventory/delete/<string:id>', methods=['DELETE'])
def delete_product(id):
    global mock_products
    p = next((p for p in mock_products if p["id"] == id), None)
    if not p:
        return("Product not found", 404)
    mock_products = [p for p in mock_products if p["id"] != id]
    return("", 204)

