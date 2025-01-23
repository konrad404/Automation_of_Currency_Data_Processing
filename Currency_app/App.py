from Currency_app.NBPDataFetcher import NBPDataFetcher
from Currency_app.DatabaseManager import DatabaseManager
from Currency_app.DataAnalyzer import DataAnalyzer
from Currency_app.ReportExporter import ReportExporter
from datetime import datetime

DB_FILE = "currency_rates.db"


class CurrencyApp:
    def __init__(self, db_file):
        self.db_manager = DatabaseManager(db_file)

    @staticmethod
    def is_valid_date(date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def fetch_data(self):
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        try:
            if CurrencyApp.is_valid_date(start_date) and CurrencyApp.is_valid_date(end_date):
                data = NBPDataFetcher.fetch_exchange_rates(start_date, end_date)
                self.db_manager.save_to_db(data)
                print("Data fetched and saved to the database.")
            else:
                raise ValueError(f"Invalid date format")
        except Exception as e:
            print(f"An error occurred while fetching data: {e}")

    def analyze_data(self):
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        try:
            if CurrencyApp.is_valid_date(start_date) and CurrencyApp.is_valid_date(end_date):
                analyzer = DataAnalyzer(self.db_manager)
                max_inc, max_dec = analyzer.analyze_data(start_date, end_date)
                print(f"Highest increase: {max_inc}")
                print(f"Biggest decrease: {max_dec}")
            else:
                raise ValueError(f"Invalid date format")
        except Exception as e:
            print(f"An error occurred while analyzing data: {e}")

    def export_report(self):
        code = input("Enter currency code for the report (e.g., 'CAD'). Leave empty for all currencies: ").strip()
        export_format = input("Choose report format (csv/json): ").strip()

        try:
            report_data = self.db_manager.fetch_data(code if code else None)
            ReportExporter.export_report(report_data, export_format)
            print("The report has been saved.")
        except Exception as e:
            print(f"An error occurred while exporting the report: {e}")

    def show_menu(self):
        while True:
            print("\n--- Currency App Menu ---")
            print("1. Fetch Exchange Rates")
            print("2. Analyze Exchange Rates")
            print("3. Export Report")
            print("4. Exit")

            choice = input("Choose an action (1-4): ").strip()

            match choice:
                case "1":
                    self.fetch_data()
                case "2":
                    self.analyze_data()
                case "3":
                    self.export_report()
                case "4":
                    print("Exiting the app...")
                    break
                case _:
                    print("Invalid choice, please try again.")


if __name__ == "__main__":
    app = CurrencyApp(DB_FILE)
    app.show_menu()
