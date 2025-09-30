import unittest
from unittest.mock import patch
from app import app

class TestFrontend(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.get')
    def test_index_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = ['test']
        mock_response.raise_for_status.return_value = None
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.requests.get')
    def test_index_backend_failure(self, mock_get):
        mock_get.side_effect = Exception('Backend down')
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()