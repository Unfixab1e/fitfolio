from django.test import TestCase, override_settings
from unittest.mock import patch
from ..api_clients import fetch_google_fit_data

class ApiClientsTest(TestCase):
    @patch('requests.post')
    def test_fetch_google_fit_data(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'data': 'some data'}
        data = fetch_google_fit_data()
        self.assertEqual(data, {'data': 'some data'})
