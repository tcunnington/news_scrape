import requests
import json
import time
import math
import itertools as itr
from ediblepickle import checkpoint

import pandas as pd

from utils import *


BASE_URL = 'https://newsapi.org/'
EVERYTHING_ENDPOINT = '/v2/everything'
SOURCES_ENDPOINT = '/v2/sources'

key_params = {
    'apiKey': '0db63d897c9844629bc477ab2639e451',
}


def get_article_data(source, date_range):

    url = BASE_URL + EVERYTHING_ENDPOINT
    date_params = {
        'from': date_range[0],  # '2017-07-01',
        'to': date_range[1],  # '2018-07-18'
    }

    page_size = 100
    page = 1
    max_page = (10000 / page_size)
    n_pages = None

    articles = []

    while n_pages is None or page < n_pages:
        other_params = {
            'sources': source['id'],
            'language': 'en',
            'pageSize': page_size,
            'page': page,
        }

        if page % 10 == 0:
            print('Page: ', page)

        params = {**date_params, **other_params, **key_params}
        response = requests.get(url, params)
        json_resp = response.json()

        if json_resp['status'] == 'ok':

            if n_pages is None:
                total_results = json_resp['totalResults']
                n_pages = math.ceil(total_results / page_size)

                if max_page < n_pages:
                    print('Unable to retrieve all articles from {source} in range ({from}-{to}). Getting first 10k.'
                          .format(source=source, **date_params))

        page += 1

        articles.extend(json_resp['articles'])

    return articles


def preload_urls(source_id, date_range):
    source = [s for s in get_sources() if s['id'] == source_id][0]
    time.sleep(0.01)  # TODO neeeedeD?
    articles = get_article_data(source, date_range)
    pd.DataFrame(articles).to_csv(get_articles_filepath(source, date_range))

def preload_urls_all_sources(overall_date_range):

    for date_range in monthly_date_ranges(overall_date_range):
        for source in get_sources():
            preload_urls(source, date_range)

#################################################
#
#     Sources
#
#################################################


# all_the_news sources
# existing_sources = {
#     'left':          ['The Atlantic','Buzzfeed','Vox',],
#     'center_left':   ['The Guardian','Washington Post','New York Times','CNN',],
#     'center':        ['NPR','Reuters'],
#     'center_right':  ['Wall Street Journal','The Hill'],
#     'right':         ['National Review','New York Post',],
#     'hyper_right':   ['Fox News','Breitbart'],
# }

sources = {
#     'hyper_left':    ['Occupy Democrats','Daily Kos'],
    'left':          ['MSNBC','Buzzfeed'], #['The Atlantic','Vox'],
    'center_left':   ['Politico','The Washington Post','The New York Times','CNN',],
    'center':        ['Reuters','Associated Press'], # ['NPR']
    'center_right':  ['The Wall Street Journal','The Hill'],
    'right':         ['National Review'], #['New York Post','The Weekly Standard','Examiner'],
    'hyper_right':   ['Fox News','Breitbart News','The American Conservative'],
}
# NPR isn't that important - have plenty of centrist docs
# MUST look into hyper left:'Occupy Democrats','Daily Kos'
# ideally also 'The Atlantic','Vox','New York Post','The Weekly Standard','Examiner',
# or find replacements
# get centrist stuff started first

sources_list = list(itr.chain(*sources.values()))


@checkpoint(key='sources.pkl', work_dir='articles/sources')
def get_sources():
    url = BASE_URL + SOURCES_ENDPOINT

    params = {
        'country': 'us',
        'language': 'en',
    }

    response = requests.get(url, {**params, **key_params})
    return [s for s in response.json()['sources'] if s['name'] in sources_list]

def get_sources_df():
    return pd.DataFrame(get_sources())

if __name__ == "__main__":
    df = get_sources_df()
    print(df)