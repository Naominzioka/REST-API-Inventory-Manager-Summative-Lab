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

def test_delete_product(client):
    response = client.delete('/inventory/delete/100')
    assert response.status_code == 204