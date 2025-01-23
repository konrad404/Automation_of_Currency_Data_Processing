import unittest
import os
import csv
import json
from Currency_app.ReportExporter import ReportExporter
import glob


class TestReportExporter(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            ("euro", "EUR", "2025-01-01", 4.50),
            ("dolar amerykański", "USD", "2025-01-01", 3.80)
        ]
        self.reports_dir = 'reports'

        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
        else:
            for file in os.listdir(self.reports_dir):
                os.remove(os.path.join(self.reports_dir, file))

    def tearDown(self):
        for file in os.listdir(self.reports_dir):
            os.remove(os.path.join(self.reports_dir, file))
        os.rmdir(self.reports_dir)

    def test_export_csv(self):
        ReportExporter.export_report(self.test_data, 'csv')

        csv_files = glob.glob(os.path.join(self.reports_dir, 'currency_report_*.csv'))
        self.assertTrue(len(csv_files) > 0)

        with open(csv_files[0], 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

            self.assertEqual(rows[0], ["Currency", "Code", "Date", "Rate"])

            self.assertEqual(rows[1], ["euro", "EUR", "2025-01-01", '4.5'])
            self.assertEqual(rows[2], ["dolar amerykański", "USD", "2025-01-01", '3.8'])

    def test_export_json(self):
        ReportExporter.export_report(self.test_data, 'json')

        json_files = glob.glob(os.path.join(self.reports_dir, 'currency_report_*.json'))
        self.assertTrue(len(json_files) > 0, "JSON file was not created")

        with open(json_files[0], 'r', encoding='utf-8') as file:
            data = json.load(file)

            expected_data = [
                {"currency": "euro", "code": "EUR", "date": "2025-01-01", "rate": 4.50},
                {"currency": "dolar amerykański", "code": "USD", "date": "2025-01-01", "rate": 3.80}
            ]
            self.assertEqual(data, expected_data)

    def test_invalid_format_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            ReportExporter.export_report(self.test_data, 'xml')

        self.assertEqual(str(context.exception), "Unsupported format: xml")


if __name__ == '__main__':
    unittest.main()
