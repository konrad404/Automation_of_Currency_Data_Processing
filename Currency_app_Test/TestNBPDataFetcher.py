import unittest
from unittest.mock import patch
import requests
from requests import HTTPError, Timeout

from Currency_app.NBPDataFetcher import NBPDataFetcher


class TestNBPDataFetcher(unittest.TestCase):
    def setUp(self):
        self.start_date = "2025-01-21"
        self.end_date = "2025-01-22"

    @patch('requests.get')
    def test_fetch_exchange_rates_success(self, mock_get):

        mock_response = {
            "table": "A",
            "no": "123/A/NBP/2025",
            "effectiveDate": "2025-01-22",
            "rates": [
                {"currency": "dolar amerykański", "code": "USD", "mid": 4.1},
                {"currency": "euro", "code": "EUR", "mid": 4.5}
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [mock_response]

        response = NBPDataFetcher.fetch_exchange_rates(self.start_date, self.end_date)

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['table'], 'A')
        self.assertEqual(response[0]['rates'][0]['code'], 'USD')
        self.assertEqual(response[0]['rates'][1]['code'], 'EUR')

    @patch('requests.get')
    def test_fetch_exchange_rates_api_error(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with self.assertRaises(HTTPError) as context:
            data = NBPDataFetcher.fetch_exchange_rates(self.start_date, self.end_date)

        self.assertEqual(str(context.exception), "404 Not Found")

    @patch('requests.get')
    def test_fetch_exchange_rates_invalid_json(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")

        with self.assertRaises(ValueError) as context:
            data = NBPDataFetcher.fetch_exchange_rates(self.start_date, self.end_date)

        self.assertEqual(str(context.exception), "Invalid JSON")

    @patch('requests.get')
    def test_fetch_exchange_rates_timeout(self, mock_get):

        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        with self.assertRaises(Timeout) as context:
            data = NBPDataFetcher.fetch_exchange_rates(self.start_date, self.end_date)

        self.assertEqual(str(context.exception), "Request timed out")


if __name__ == '__main__':
    unittest.main()
