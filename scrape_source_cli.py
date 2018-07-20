import argparse
from newspaper_scrape import scrape


parser = argparse.ArgumentParser(description='Scrape a single source')


parser.add_argument('source')
parser.add_argument('--from', default='2018-07-18', help="from date in format '2017-07-18'")
parser.add_argument('--to', default='2018-07-01', help="to date in format '2017-07-18'")

args = parser.parse_args()

overall_date_range = (args['from'], args['to'])

scrape([args.source], overall_date_range)

