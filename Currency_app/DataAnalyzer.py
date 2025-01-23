import sqlite3
import pandas as pd

class DataAnalyzer:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def analyze_data(self, start_date, end_date):
        connection = sqlite3.connect(self.db_manager.db_file)
        cursor = connection.cursor()
        cursor.execute('''
            WITH ranked_rates AS (
                SELECT 
                    code, 
                    rate, 
                    date,
                    ROW_NUMBER() OVER (PARTITION BY code ORDER BY date ASC) AS first_occurrence,
                    ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) AS last_occurrence
                FROM exchange_rates
                WHERE date BETWEEN ? AND ?
            )
            SELECT 
                code, 
                ROUND(MAX(CASE WHEN last_occurrence = 1 THEN rate END) - 
                    MAX(CASE WHEN first_occurrence = 1 THEN rate END), 10) as change
            FROM ranked_rates
            GROUP BY code
            ORDER BY change DESC LIMIT 1
        ''', (start_date, end_date))

        max_increase = cursor.fetchone()

        cursor.execute('''
                    WITH ranked_rates AS (
                        SELECT 
                            code, 
                            rate, 
                            date,
                            ROW_NUMBER() OVER (PARTITION BY code ORDER BY date ASC) AS first_occurrence,
                            ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) AS last_occurrence
                        FROM exchange_rates
                        WHERE date BETWEEN ? AND ?
                    )
                    SELECT 
                        code, 
                        ROUND(MAX(CASE WHEN last_occurrence = 1 THEN rate END) - 
                            MAX(CASE WHEN first_occurrence = 1 THEN rate END), 10) as change
                    FROM ranked_rates
                    GROUP BY code
                    ORDER BY change ASC LIMIT 1
                ''', (start_date, end_date))

        max_decrease = cursor.fetchone()

        # cursor.execute('''
        #             SELECT
        #                 code,
        #                 rate,
        #                 date,
        #                 ROW_NUMBER() OVER (PARTITION BY code ORDER BY date ASC) AS first_occurrence
        #             FROM exchange_rates
        #             WHERE date BETWEEN ? AND ?
        #         ''', (start_date, end_date))
        #
        # tmp = cursor.fetchall()
        # print(tmp)

        connection.close()

        return max_increase, max_decrease