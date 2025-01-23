import unittest
import os
from datetime import datetime

from Currency_app.DataAnalyzer import DataAnalyzer
from Currency_app.DatabaseManager import DatabaseManager

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.db_file = f'test_db_{datetime.now().strftime("%Y%m%d%H%M%S")}.db'
        self.db_manager = DatabaseManager(self.db_file)

        self.test_data = [
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
                    {"currency": "euro", "code": "EUR", "mid": 4.0},
                ]
            },
            {
                "effectiveDate": "2025-01-22",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 3.7},
                    {"currency": "euro", "code": "EUR", "mid": 4.1},
                ]
            }
        ]

        self.db_manager.save_to_db(self.test_data)
        self.analyzer = DataAnalyzer(self.db_manager)

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_analyze_data_max_increase(self):
        max_increase, _ = self.analyzer.analyze_data("2025-01-20", "2025-01-22")
        print(max_increase)
        self.assertEqual(max_increase[0], "USD")  # USD should have the highest increase
        self.assertEqual(max_increase[1], 0.2)    # 3.7 (last) - 3.5 (first) = 0.2

    def test_analyze_data_max_decrease(self):
        _, max_decrease = self.analyzer.analyze_data("2025-01-20", "2025-01-22")
        self.assertEqual(max_decrease[0], "EUR")  # EUR should have the biggest decrease
        self.assertEqual(max_decrease[1], -0.1)   # 4.1 (last) - 4.2 (first) = -0.1

    def test_no_data_in_range(self):
        max_increase, max_decrease = self.analyzer.analyze_data("2025-01-01", "2025-01-03")
        self.assertEqual(max_increase, None)
        self.assertEqual(max_decrease, None)

    def test_single_day_range(self):
        max_increase, max_decrease = self.analyzer.analyze_data("2025-01-22", "2025-01-22")
        self.assertEqual(max_increase[1], 0)  # No change in rate if single day selected
        self.assertEqual(max_decrease[1], 0)

if __name__ == '__main__':
    unittest.main()
