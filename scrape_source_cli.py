import argparse
from news_api import preload_urls, preload_urls_all_sources


parser = argparse.ArgumentParser(description='Scrape a single source')


parser.add_argument('source')
parser.add_argument('from', default='2017-07-18', help="from date in format '2017-07-18'")
parser.add_argument('to', default='2017-06-01', help="to date in format '2017-07-18'")

args = parser.parse_args()

overall_date_range = (args['from'], args['to'])

