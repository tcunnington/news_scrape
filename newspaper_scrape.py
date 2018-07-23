# import os

# import requests
# import json
# import math
import time
import random
import pandas as pd
from datetime import datetime, timedelta

from ediblepickle import checkpoint
from retrying import retry

import newspaper
from newspaper import Article
from newspaper.article import ArticleException, ArticleDownloadState

from utils import *

## something like this is you want to implement multicore stuff here...
# my_sources = []
# for source in my_sources:
#     # define time intervals, stored in table maybe?
#     # run scrape for each interval
#     date_range = ()
#
#     df = scrape_source(source, date_range)




# Suggest you wrap this in try/catch
@retry(wait_random_min=500, wait_random_max=1000, stop_max_attempt_number=2)
def scrape_url(url):

    article = Article(url)
    article.download()
    if article.download_state == ArticleDownloadState.FAILED_RESPONSE:
        print(article.download_exception_msg)
    article.parse()

    return article.title, article.text


@checkpoint(key=lambda args, kwargs: resolve_source_key(args[0]) + resolve_date_key(args[1]) + '.pkl',
            work_dir='articles/cache')
def scrape_batch(source, date_range): # Note these are the input due to making edible pickling easy
    # get urls from saved article metadata

    print('batch scrape', source, date_range)

    filepath = get_articles_filepath(source, date_range)
    df = pd.read_csv(filepath)

    print(filepath)
    print(df.head())

    if 'content' not in df.columns:
        df['content'] = ''

    count = 0
    error_count = 0

    for row in df[:10]: # TODO OOASDFASDFADSF
        url = row.url

        time.sleep(random.random() + 0.1)

        try:
            title, text = scrape_url(url)
        except ArticleException as e:
            # If the download for some reason fails (ex. 404) the script will continue
            print(e)
            print("Scrape errorrrrrrrr...")
            error_count += 1
            continue

        row['content'] = text
        count += 1

    print("{} articles downloaded from {} ({} errors counted)".format(count, source, error_count))

    # have to return the item to pickle!!
    return df


def scrape(source_ids, overall_date_range):
    for date_range in monthly_date_ranges(overall_date_range):
        for source_id in source_ids:
            scrape_batch(source_id, date_range)


if __name__ == "__main__":
     # Test..
    print(resolve_source_key('the-washington-post'))
    print(resolve_source_key('cnn'))
    print(resolve_source_key('fox-news'))

    dates = ('2017-07-01','2018-07-18')
    print(resolve_date_key(dates))

    print(get_articles_filepath('the-washington-post', dates))

    scrape_url('http://www.bbc.co.uk/news/world-us-canada-44868069')