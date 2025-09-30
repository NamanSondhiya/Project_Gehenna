import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.requests.get')
def test_index_success(mock_get, client):
    mock_response = MagicMock()
    mock_response.json.return_value = ['John', 'Jane']
    mock_get.return_value = mock_response

    response = client.get('/')
    assert response.status_code == 200
    assert b'John' in response.data
    assert b'Jane' in response.data

@patch('app.requests.get')
def test_index_failure(mock_get, client):
    mock_get.side_effect = Exception('Connection error')

    response = client.get('/')
    assert response.status_code == 200
    # Should render page with empty data
    assert b'No entries found' in response.data or b'[]' in response.data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
