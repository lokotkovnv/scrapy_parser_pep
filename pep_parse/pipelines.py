import datetime as dt
import os
import csv
from pep_parse.settings import BASE_DIR, RESULTS


class PepParsePipeline:

    def __init__(self):
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)
        self.status_counts = {}
        self.total_peps = 0
        self.output_file = None

    def open_spider(self, spider):
        current_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{current_time}.csv'
        output_path = os.path.join(self.results_dir, filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.output_file = open(
            output_path, mode='w', encoding='utf-8', newline=''
        )
        self.csv_writer = csv.DictWriter(
            self.output_file, fieldnames=['Статус', 'Количество']
        )
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        status = item.get('status')
        if status not in self.status_counts:
            self.status_counts[status] = 0
        self.status_counts[status] += 1
        self.total_peps += 1

        return item

    def close_spider(self, spider):
        for status, count in self.status_counts.items():
            self.csv_writer.writerow({'Статус': status, 'Количество': count})

        self.csv_writer.writerow(
            {'Статус': 'Total', 'Количество': self.total_peps}
        )

        if self.output_file:
            self.output_file.close()
