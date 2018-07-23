#!/bin/bash
# A script to run 4 times a day to hit news api

cd ~/capstone/news_scrape/

/opt/conda/envs/scrape/bin/python save_article_urls_cli.py '2018-06-10' '2018-07-18'
