import psycopg2
import json
from psycopg2.errors import UndefinedTable
from psycopg2.extras import execute_values

class DBConfig: 
    def __init__(self, config_dict=None):
        if not config_dict:
            self.dbname='twitter'
            self.host='localhost'
            self.user='postgres'
            self.password='bobolo'
        else:
            raise NotImplemented()

def save_tweets(tweets: [], config):
    """A function which pushes tweet dicts to a db"""

    json_tweets = [(json.dumps(tweet),) for tweet in tweets]
    try:
        with _get_connection(config) as conn:
            with conn.cursor() as cur:
                insert_query = """INSERT INTO tweet (data) VALUES %s;"""
                execute_values(cur, insert_query, json_tweets)
                conn.commit()
    except UndefinedTable as e:
        print('Table unavailable, creating it..')
        _create_tweet_table(config)
        save_tweets(tweets, config)

def _create_tweet_table(config):
    with _get_connection(config) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE tweet(id SERIAL PRIMARY KEY, data JSON);")
                conn.commit()

def _get_connection(config):
    return psycopg2.connect(
            dbname=config.dbname,
            host=config.host,
            user=config.user,
            password=config.password
        )    

def read_tweets(config):
    """A function which pulls all tweet dicts from a db"""

    with _get_connection(config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT data FROM tweet;")
            rows = cur.fetchall()
            return list(map(lambda x: x[0], rows))

def clear_tweet_table(config):
    """A function which clears the tweet table"""
    with _get_connection(config) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tweet;")
            conn.commit()