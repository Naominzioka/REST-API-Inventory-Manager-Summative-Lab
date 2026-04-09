import pytest
from unittest.mock import patch
from app.routes import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        test_data = [
            {"id": "100", "name": "Test Snack", "count": 1, "brand": "Generic"}
        ]
        with patch('app.routes.mock_products', test_data):
            yield client

def test_inventory(client):
    response = client.get('/inventory')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == "100"

def test_get_inventory_id(client):
    response = client.get('/inventory/100')
    assert response.status_code == 200
    assert response.get_json()['name'] == "Test Snack"


@patch('app.routes.fetch_product_by_barcode')
def test_get_inventory_id_fetches_external_when_missing(mock_fetch, client):
    mock_fetch.return_value = {
        "id": "555",
        "name": "Juice",
        "count": 1,
    }

    response = client.get('/inventory/555')

    assert response.status_code == 200
    assert response.get_json()['name'] == "Juice"
    mock_fetch.assert_called_once_with('555')

def test_add_new_product(client):
    response = client.post('/inventory/add', json={"name": "New Item"})
    assert response.status_code == 201
    assert response.get_json()['id'] == "101"


def test_add_new_product_missing_name(client):
    response = client.post('/inventory/add', json={})

    assert response.status_code == 400
    assert response.get_json()['error'] == "Product name is required"


def test_add_new_product_blank_name(client):
    response = client.post('/inventory/add', json={"name": "   "})

    assert response.status_code == 400
    assert response.get_json()['error'] == "Product name cannot be empty"


def test_add_new_product_invalid_json(client):
    response = client.post(
        '/inventory/add',
        data='{"name": ',
        content_type='application/json',
    )

    assert response.status_code == 400
    assert response.get_json()['error'] == "Product name is required"


def test_update_stock_invalid_quantity(client):
    response = client.patch('/inventory/update/100/0')

    assert response.status_code == 400
    assert response.get_json()['error'] == "Quantity must be greater than 0"

def test_delete_product(client):
    response = client.delete('/inventory/delete/100')
    assert response.status_code == 204