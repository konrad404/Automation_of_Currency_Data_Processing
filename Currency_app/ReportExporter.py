import csv
import json
import os
from datetime import datetime


class ReportExporter:
    @staticmethod
    def export_report(data, export_format):

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        directory = 'reports'
        if not os.path.exists(directory):
            os.makedirs(directory)

        if export_format == 'csv':
            filename = os.path.join(directory, f'currency_report_{timestamp}.csv')
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Currency", "Code", "Date", "Rate"])
                writer.writerows(data)
                file.flush()
        elif export_format == 'json':
            filename = os.path.join(directory, f'currency_report_{timestamp}.json')
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump([{"currency": row[0], "code": row[1], "date": row[2], "rate": row[3]} for row in data], file,
                          indent=4, ensure_ascii=False)
                file.flush()
        else:
            raise ValueError(f"Unsupported format: {export_format}")