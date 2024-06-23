from pathlib import Path

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

BASE_DIR = Path(__file__).parent.parent

RESULTS = 'results'
RESULTS_DIR = BASE_DIR / RESULTS

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

FILE_FORMAT = 'csv'

PEP_NAME = 'pep'
PEP_FILE_NAME = f'{PEP_NAME}_%(time)s.{FILE_FORMAT}'

PEPS_DOMAIN = 'peps.python.org'
PEPS_URL = 'https://peps.python.org/'


FEEDS = {
    f'{RESULTS}/{PEP_FILE_NAME}': {
        'format': FILE_FORMAT,
        'fields': ['number', 'name', 'status'],
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
