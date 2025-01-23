import requests

API_URL = "http://api.nbp.pl/api/exchangerates/tables/A/"

class NBPDataFetcher:
    @staticmethod
    def fetch_exchange_rates(start_date, end_date):
        url = f"{API_URL}{start_date}/{end_date}/?format=json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching data from {API_URL}: {e}")
            raise e

