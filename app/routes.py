from flask import Flask, jsonify, request
from app import mock_products as inventory_data

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
        for p in inventory_data.mock_products
    ]
    return jsonify(items)

#route to get a particular product
@app.route('/inventory/<string:id>', methods=['GET'])
def get_inventory_id(id):
    for p in inventory_data.mock_products:
        if p['id'] == id:
            item = {'id': p['id'], 'name': p['name'], 'count': p['count']}
            return jsonify(item), 200

    fetched_product = inventory_data.fetch_product_by_barcode(id)
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
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or 'name' not in data:
        return jsonify({"error": "Product name is required"}), 400

    product_name = data.get('name', '')
    if not isinstance(product_name, str) or not product_name.strip():
        return jsonify({"error": "Product name cannot be empty"}), 400
    
    new_product = inventory_data.add_new_product(product_name)
    return jsonify(new_product), 201

#route to update stock of an existing product    
@app.route('/inventory/update/<string:id>/<int:qty>', methods=['PATCH'])
def update_stock(id, qty):
    if qty <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400

    added_item = inventory_data.add_to_stock(id, qty)
    if added_item:
        return jsonify({"message": f"Added {qty} units",
                       "product": added_item['name'],
                       "new_total": added_item['count']})
        
    return jsonify({"error": "Product not found"}), 404

#delete a product
@app.route('/inventory/delete/<string:id>', methods=['DELETE'])
def delete_product(id):
    if not inventory_data.delete_product_by_id(id):
        return jsonify({"error": "Product not found"}), 404
    return ("", 204)

