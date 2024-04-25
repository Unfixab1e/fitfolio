from django.test import TestCase
from unittest.mock import patch
from ..tasks import update_health_data

class IntegrationTest(TestCase):
    @patch('fitfolio.api_clients.fetch_google_fit_data')
    @patch('fitfolio.api_clients.fetch_samsung_health_data')
    def test_update_health_data(self, mock_google, mock_samsung):
        mock_google.return_value = {'steps': 1000}
        mock_samsung.return_value = {'steps': 800}
        update_health_data()
        # Add assertions here as needed
