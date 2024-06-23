import csv
import datetime as dt
import os
from collections import defaultdict

from pep_parse.settings import BASE_DIR, RESULTS


class PepParsePipeline:

    def open_spider(self, spider):
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)

        self.status_counts = defaultdict(int)

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
        self.status_counts[status] += 1

        return item

    def close_spider(self, spider):
        for status, count in self.status_counts.items():
            self.csv_writer.writerow({'Статус': status, 'Количество': count})

        total_peps = sum(self.status_counts.values())
        self.csv_writer.writerow({'Статус': 'Total', 'Количество': total_peps})

        if self.output_file:
            self.output_file.close()
