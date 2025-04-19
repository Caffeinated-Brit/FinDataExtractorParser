import os
import pytest
from main import app
from unittest.mock import patch

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_full_parse():
    """Mock fullParse method"""
    with patch('parse.fullParse', return_value=[{"key": "value"}]) as mock:
        yield mock

def test_parse_pdf_success(client, mock_full_parse):
    """Test successful parsing using existing pdf"""
    pdf_path = os.path.join(os.path.dirname(__file__), "Simple_Mock_Data.pdf")

    assert os.path.exists(pdf_path), f"Test PDF not found: {pdf_path}"

    with open(pdf_path, "rb") as file:
        data = {'file': (file, 'Simple_Mock_Data.pdf')}
        response = client.post('/parse', data=data, content_type='multipart/form-data')

    assert response.status_code == 200, f"Unexpected response: {response.json}"
    assert response.json == {
        "message": "File uploaded and processed successfully!",
        'data': {'address': '1234 whocare lane', 'date': '11/29/2024', 'name': 'Lukas Maynard'}
    }

# this took forever to figure out...
# this needed to patch main.fullParse and not parse.fullParse because main.py uses "from parse import fullParse"
@patch('main.fullParse', side_effect=Exception("Error in parsing PDF"))
@patch('os.remove')  # Prevents accidental file deletions
def test_parse_pdf_failure(mock_full_parse, mock_remove, client):
    """Test when fullParse raises an exception"""
    pdf_path = os.path.join(os.path.dirname(__file__), "Simple_Mock_Data.pdf")

    assert os.path.exists(pdf_path), f"Test PDF not found: {pdf_path}"

    with open(pdf_path, "rb") as file:
        data = {'file': (file, 'Simple_Mock_Data.pdf')}
        response = client.post('/parse', data=data, content_type='multipart/form-data')

    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json)

    assert response.status_code == 500
    assert response.json == {"error": "Error in parsing PDF"}
