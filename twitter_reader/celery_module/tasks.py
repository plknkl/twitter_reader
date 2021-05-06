from .celery import app

import sys
sys.path.append("..")

from twitter_manager.component import APIConfig, APIManager
from data_storer.component import DBConfig, DBManager

@app.task
def query_tweets(query):
    tm_conf = APIConfig()
    tm = APIManager(tm_conf)
    tweets = tm.query(query, pages=1)
    db_config = DBConfig()
    dman = DBManager(db_config)
    dman.save_tweets(tweets)
    return f'Got {len(tweets)} tweets'