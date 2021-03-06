import psycopg2
import json
from psycopg2.errors import UndefinedTable
from psycopg2.extras import execute_values

class DBConfig: 
    def __init__(self, config_dict=None):
        if not config_dict:
            self.dbname='twitter'
            self.host='db'
            self.user='postgres'
            self.password='bobolo'
        else:
            raise NotImplemented()

class DBManager:
    def __init__(self, config: DBConfig):
        self.config = config

    def save_tweets(self, tweets: []) -> None:
        """A function which pushes tweet dicts to a db"""
        json_tweets = [(json.dumps(tweet.raw),) for tweet in tweets]
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    insert_query = """INSERT INTO tweet (data) VALUES %s;"""
                    execute_values(cur, insert_query, json_tweets)
                    conn.commit()
        except UndefinedTable as e:
            print('Table unavailable, creating it..')
            self._create_tweet_table()
            self.save_tweets(tweets)

    def _create_tweet_table(self):
        with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE TABLE tweet(id SERIAL PRIMARY KEY, data JSON);")
                    conn.commit()

    def _get_connection(self):
        return psycopg2.connect(
                dbname=self.config.dbname,
                host=self.config.host,
                user=self.config.user,
                password=self.config.password
            )    

    def read_tweets(self) -> []:
        """A function which pulls all tweet dicts from a db"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT data FROM tweet;")
                rows = cur.fetchall()
                return list(map(lambda x: x[0], rows))

    def clear_tweet_table(self) -> None:
        """A function which clears the tweet table"""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tweet;")
                conn.commit()