import unittest
import sqlite3
import os
from datetime import datetime
from Currency_app.DatabaseManager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        """Create a temporary database file"""
        self.db_file = f'test_db_{datetime.now().strftime("%Y%m%d%H%M%S")}.db'
        self.db_manager = DatabaseManager(self.db_file)

    def tearDown(self):
        """Remove the database file after the test."""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_init_db_creates_table(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='exchange_rates'")
        result = cursor.fetchone()
        connection.close()

        print(result)

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'exchange_rates')

    def test_save_to_db_inserts_data(self):
        data = [
            {
                "effectiveDate": "2025-01-22",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 1.1},
                    {"currency": "euro", "code": "EUR", "mid": 0.9},
                ]
            }
        ]

        self.db_manager.save_to_db(data)

        fetched_data = self.db_manager.fetch_data()

        self.assertEqual(len(fetched_data), 2)
        self.assertEqual(fetched_data[0], ('dolar amerykański', 'USD', '2025-01-22', 1.1))
        self.assertEqual(fetched_data[1], ('euro', 'EUR', '2025-01-22', 0.9))

    def test_fetch_data_with_code(self):
        data = [
            {
                "effectiveDate": "2025-01-22",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 1.1},
                    {"currency": "euro", "code": "EUR", "mid": 0.9},
                ]
            }
        ]

        self.db_manager.save_to_db(data)

        fetched_data = self.db_manager.fetch_data('USD')

        self.assertEqual(len(fetched_data), 1)
        self.assertEqual(fetched_data[0], ('dolar amerykański', 'USD', '2025-01-22', 1.1))

    def test_duplicate_security(self):
        data = [
            {
                "effectiveDate": "2025-01-22",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 1.1},
                    {"currency": "euro", "code": "EUR", "mid": 0.9},
                ]
            },
            {
                "effectiveDate": "2025-01-22",
                "rates": [
                    {"currency": "dolar amerykański", "code": "USD", "mid": 1.1},
                    {"currency": "dolar australijski", "code": "AUD", "mid": 2.5},
                ]
            }
        ]

        self.db_manager.save_to_db(data)

        fetched_data = self.db_manager.fetch_data()

        self.assertEqual(len(fetched_data), 3)
        self.assertEqual(fetched_data[0], ('dolar amerykański', 'USD', '2025-01-22', 1.1))
        self.assertEqual(fetched_data[1], ('euro', 'EUR', '2025-01-22', 0.9))
        self.assertEqual(fetched_data[2], ('dolar australijski', 'AUD', '2025-01-22', 2.5))

if __name__ == '__main__':
    unittest.main()
