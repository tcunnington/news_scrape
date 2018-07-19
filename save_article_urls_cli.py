import argparse
from news_api import preload_urls, preload_urls_all_sources


parser = argparse.ArgumentParser(description='Get urls from News API')

parser.add_argument('from_date', default='2017-07-18', help="from date in format '2017-07-18'")
parser.add_argument('to_date', default='2017-06-01', help="to date in format '2017-07-18'")
parser.add_argument('-s','--source', help="Single source to run")

args = parser.parse_args()

overall_date_range = (args.from_date, args.to_date)

if not args.source:
    print('Are you sure you want to get urls for all sources? date range = {}'.format(str(overall_date_range)))
    answer = input("[y]/n")

    if answer == '' or answer == 'y':
        preload_urls_all_sources(overall_date_range)
else:
    preload_urls(args.source, overall_date_range)
