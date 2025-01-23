import csv
import glob
import json
import os.path
import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch

from Currency_app.App import CurrencyApp


class TestApp(unittest.TestCase):
    def setUp(self):
        self.db_file = f'test_db_{datetime.now().strftime("%Y%m%d%H%M%S")}.db'
        self.app = CurrencyApp(self.db_file)
        self.db_manager = self.app.db_manager
        self.reports_dir = 'reports'

        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
        else:
            for file in os.listdir(self.reports_dir):
                os.remove(os.path.join(self.reports_dir, file))

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

        for file in os.listdir(self.reports_dir):
            os.remove(os.path.join(self.reports_dir, file))
        os.rmdir(self.reports_dir)

    def save_complex_data_to_db(self):
        test_data = [
            {
                "effectiveDate": "2025-01-20",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 3.5},
                    {"currency": "euro", "code": "EUR", "mid": 4.2},
                ]
            },
            {
                "effectiveDate": "2025-01-21",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 3.6},
                    {"currency": "euro", "code": "EUR", "mid": 3.9},
                ]
            },
            {
                "effectiveDate": "2025-01-22",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 3.8},
                    {"currency": "euro", "code": "EUR", "mid": 4.0},
                ]
            }
        ]

        self.db_manager.save_to_db(test_data)

    @patch('requests.get')
    @patch('builtins.input', side_effect=['2025-01-20', '2025-01-22'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_fetch_data_add_correct_data_to_db(self, mock_stdout, mock_input, mock_get):
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

        self.app.fetch_data()
        output = mock_stdout.getvalue().strip()

        self.assertEqual(output, "Data fetched and saved to the database.")

        db_content = self.db_manager.fetch_data()

        self.assertEqual(len(db_content), 2)
        self.assertEqual(db_content[0], ('dolar amerykański', 'USD', '2025-01-22', 4.1))
        self.assertEqual(db_content[1], ('euro', 'EUR', '2025-01-22', 4.5))


    @patch('builtins.input', side_effect=['2025-01-20', '2025-31-22'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_fetch_data_with_incorrect_date_format(self, mock_stdout, mock_input):
        self.app.fetch_data()
        output = mock_stdout.getvalue().strip()

        self.assertEqual(output, "An error occurred while fetching data: Invalid date format")

    @patch('builtins.input', side_effect=['2025-01-20', '2025-01-22'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_analyze_data_return_correct_data(self, mock_stdout, mock_input):

        self.save_complex_data_to_db()
        self.app.analyze_data()
        output = mock_stdout.getvalue()

        self.assertEqual(output, "Highest increase: ('USD', 0.3)\nBiggest decrease: ('EUR', -0.2)\n")


    @patch('builtins.input', side_effect=['2025-01-20', '2025-31-22'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_analyze_data_with_incorrect_date_format(self, mock_stdout, mock_input):
        self.app.analyze_data()
        output = mock_stdout.getvalue().strip()

        self.assertEqual(output, "An error occurred while analyzing data: Invalid date format")


    @patch('builtins.input', side_effect=['', 'csv'])
    def test_export_reports_csv_format(self, mock_input):
        self.save_complex_data_to_db()
        self.app.export_report()

        csv_files = glob.glob(os.path.join(self.reports_dir, 'currency_report_*.csv'))
        self.assertTrue(len(csv_files) > 0)

        with open(csv_files[0], 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 7)

            self.assertEqual(rows[0], ["Currency", "Code", "Date", "Rate"])

            self.assertEqual(rows[1], ["dolar amerykański", "USD", "2025-01-20", '3.5'])
            self.assertEqual(rows[2], ["euro", "EUR", "2025-01-20", '4.2'])
            self.assertEqual(rows[3], ["dolar amerykański", "USD", "2025-01-21", '3.6'])
            self.assertEqual(rows[4], ["euro", "EUR", "2025-01-21", '3.9'])
            self.assertEqual(rows[5], ["dolar amerykański", "USD", "2025-01-22", '3.8'])
            self.assertEqual(rows[6], ["euro", "EUR", "2025-01-22", '4.0'])

    @patch('builtins.input', side_effect=['USD', 'csv'])
    def test_export_reports_csv_format_single_currency_code(self, mock_input):
        self.save_complex_data_to_db()
        self.app.export_report()

        csv_files = glob.glob(os.path.join(self.reports_dir, 'currency_report_*.csv'))
        self.assertTrue(len(csv_files) > 0)

        with open(csv_files[0], 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 4)

            self.assertEqual(rows[0], ["Currency", "Code", "Date", "Rate"])

            self.assertEqual(rows[1], ["dolar amerykański", "USD", "2025-01-20", '3.5'])
            self.assertEqual(rows[2], ["dolar amerykański", "USD", "2025-01-21", '3.6'])
            self.assertEqual(rows[3], ["dolar amerykański", "USD", "2025-01-22", '3.8'])

    @patch('builtins.input', side_effect=['', 'json'])
    def test_export_reports_json_format(self, mock_input):
        self.save_complex_data_to_db()
        self.app.export_report()

        json_files = glob.glob(os.path.join(self.reports_dir, 'currency_report_*.json'))
        self.assertTrue(len(json_files) > 0)

        with open(json_files[0], 'r', encoding='utf-8') as file:
            data = json.load(file)

            expected_data = [
                {"currency": "dolar amerykański", "code": "USD", "date": "2025-01-20", "rate": 3.5},
                {"currency": "euro", "code": "EUR", "date": "2025-01-20", "rate": 4.2},
                {"currency": "dolar amerykański", "code": "USD", "date": "2025-01-21", "rate": 3.6},
                {"currency": "euro", "code": "EUR", "date": "2025-01-21", "rate": 3.9},
                {"currency": "dolar amerykański", "code": "USD", "date": "2025-01-22", "rate": 3.8},
                {"currency": "euro", "code": "EUR", "date": "2025-01-22", "rate": 4.0}
            ]
            self.assertEqual(data, expected_data)


    @patch('builtins.input', side_effect=['USD', 'json'])
    def test_export_reports_json_format_single_currency_code(self, mock_input):
        self.save_complex_data_to_db()
        self.app.export_report()

        json_files = glob.glob(os.path.join(self.reports_dir, 'currency_report_*.json'))
        self.assertTrue(len(json_files) > 0)

        with open(json_files[0], 'r', encoding='utf-8') as file:
            data = json.load(file)

            expected_data = [
                {"currency": "dolar amerykański", "code": "USD", "date": "2025-01-20", "rate": 3.5},
                {"currency": "dolar amerykański", "code": "USD", "date": "2025-01-21", "rate": 3.6},
                {"currency": "dolar amerykański", "code": "USD", "date": "2025-01-22", "rate": 3.8}
            ]
            self.assertEqual(data, expected_data)


    @patch('builtins.input', side_effect=['SSS', 'json'])
    def test_export_reports_incorrect_currency_code(self, mock_input):
        self.save_complex_data_to_db()
        self.app.export_report()

        json_files = glob.glob(os.path.join(self.reports_dir, 'currency_report_*.json'))
        self.assertTrue(len(json_files) > 0)

        with open(json_files[0], 'r', encoding='utf-8') as file:
            data = json.load(file)

            expected_data = []
            self.assertEqual(data, expected_data)


    @patch('builtins.input', side_effect=['USD', 'sss'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_export_reports_incorrect_file_format_exception(self,mock_stdout, mock_input):
        self.save_complex_data_to_db()
        self.app.export_report()

        output = mock_stdout.getvalue().strip()

        self.assertEqual(output, "An error occurred while exporting the report: Unsupported format: sss")