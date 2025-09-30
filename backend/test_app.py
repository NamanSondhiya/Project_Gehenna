import unittest
from unittest.mock import patch, MagicMock
import json
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_root_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

    @patch('app.get_collection')
    def test_get_names_success(self, mock_get_collection):
        mock_coll = MagicMock()
        mock_coll.find.return_value = [{'name': 'test'}]
        mock_get_collection.return_value = mock_coll
        
        response = self.app.get('/api/get')
        self.assertEqual(response.status_code, 200)

    @patch('app.get_collection')
    def test_add_name_success(self, mock_get_collection):
        mock_coll = MagicMock()
        mock_coll.find_one.return_value = None
        mock_coll.insert_one.return_value = None
        mock_get_collection.return_value = mock_coll
        
        response = self.app.post('/api/add', 
                                json={'name': 'test'},
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_add_name_invalid(self):
        response = self.app.post('/api/add', 
                                json={'name': ''},
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()