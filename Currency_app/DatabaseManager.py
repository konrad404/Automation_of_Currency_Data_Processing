import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS exchange_rates (
                            currency TEXT,
                            code TEXT,
                            date TEXT,
                            rate REAL,
                            PRIMARY KEY (code, date))''')
        connection.commit()
        connection.close()

    def save_to_db(self, data):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        for day in data:
            date = day["effectiveDate"]
            for rate in day["rates"]:
                cursor.execute('''INSERT OR IGNORE INTO exchange_rates (currency, code, date, rate)
                                  VALUES (?, ?, ?, ?)''',
                               (rate["currency"], rate["code"], date, rate["mid"]))
        connection.commit()
        connection.close()

    def fetch_data(self, code=None):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        if code:
            cursor.execute("SELECT * FROM exchange_rates WHERE code = ? ORDER BY date", (code,))
        else:
            cursor.execute("SELECT * FROM exchange_rates ORDER BY date")

        data = cursor.fetchall()
        conn.close()
        return data