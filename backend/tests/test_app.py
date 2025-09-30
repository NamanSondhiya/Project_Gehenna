import pytest
from app import app, validate_name

def test_validate_name():
    assert validate_name("John Doe") == (True, "John Doe")
    assert validate_name("") == (False, "Name is required and must be a string")
    assert validate_name("   ") == (False, "Name must be between 1 and 50 characters")
    assert validate_name("John123") == (False, "Name can only contain letters and spaces")
    assert validate_name("a" * 51) == (False, "Name must be between 1 and 50 characters")

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "service": "backend"}

def test_get_names_empty(client):
    response = client.get('/api/get')
    assert response.status_code == 200
    assert response.get_json() == []

def test_add_name(client):
    response = client.post('/api/add/John')
    assert response.status_code == 200
    assert "added successfully" in response.get_json()['message']

def test_add_duplicate_name(client):
    client.post('/api/add/John')
    response = client.post('/api/add/John')
    assert response.status_code == 409
    assert "already exists" in response.get_json()['error']

def test_add_invalid_name(client):
    response = client.post('/api/add/123')
    assert response.status_code == 400
    assert "can only contain letters" in response.get_json()['error']

def test_get_names_after_add(client):
    client.post('/api/add/John')
    client.post('/api/add/Jane')
    response = client.get('/api/get')
    assert response.status_code == 200
    data = response.get_json()
    assert "John" in data
    assert "Jane" in data

def test_delete_name(client):
    client.post('/api/add/John')
    response = client.delete('/api/delete/John')
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()['message']

def test_delete_nonexistent_name(client):
    response = client.delete('/api/delete/Nonexistent')
    assert response.status_code == 404
    assert "not found" in response.get_json()['error']

def test_search_names(client):
    client.post('/api/add/John')
    client.post('/api/add/Jane')
    client.post('/api/add/Bob')
    response = client.get('/api/search/Jo')
    assert response.status_code == 200
    data = response.get_json()
    assert "John" in data
    assert "Jane" not in data

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == "ok"
