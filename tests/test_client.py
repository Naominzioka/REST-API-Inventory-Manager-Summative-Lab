import pytest
from unittest.mock import patch, MagicMock
from CLI import handlers 

class MockArgs:
    """A helper class to simulate argparse arguments."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@patch('CLI.handlers.requests.get')
def test_fetch_product_logic(mock_get, capsys):
    """Test the fetch-product CLI command output."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"name": "Juice", "count": 5}
    mock_get.return_value = mock_resp

    args = MockArgs(barcode="555")
    handlers.fetch_product({}, args)

    captured = capsys.readouterr()
    assert "Found Juice | Stock 5" in captured.out

@patch('CLI.handlers.requests.patch')
def test_restock_handler(mock_patch, capsys):
    """Test the restock-product CLI command output."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "message": "Added 5 units",
        "product": "Soda",
        "new_total": 15
    }
    mock_patch.return_value = mock_resp

    args = MockArgs(product_id="100", quantity=5)
    handlers.restock_product({}, args)

    captured = capsys.readouterr()
    assert "New total is 15" in captured.out

@patch('CLI.handlers.requests.delete')
def test_delete_product_cli(mock_delete, capsys):
    """Test the delete-product CLI command success message."""
    mock_resp = MagicMock()
    mock_resp.status_code = 204
    mock_delete.return_value = mock_resp

    args = MockArgs(product_id="100")
    # Mocking view_products inside delete_product to avoid errors
    with patch('CLI.handlers.view_products'):
        handlers.delete_product({}, args)

    captured = capsys.readouterr()
    assert "Successfully deleted product 100" in captured.out