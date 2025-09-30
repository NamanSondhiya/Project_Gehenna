import pytest
from mongomock import MongoClient
import os
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    # Mock the MongoClient in connection.py
    mock_client = MongoClient()
    mock_db = mock_client['test_gehenna']
    mock_coll = mock_db['test_names']

    def mock_mongo_client(*args, **kwargs):
        return mock_client

    monkeypatch.setattr('connection.MongoClient', mock_mongo_client)
    monkeypatch.setattr('connection.db', mock_db)
    monkeypatch.setattr('connection.coll', mock_coll)

    # Clear collection before each test
    mock_coll.delete_many({})
