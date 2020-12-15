import sqlite3
import re

class DBManager:

    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        conn = sqlite3.connect('./db/db.sqlite3')
        return conn

    def reset_raw_tweets(self):
        c = self.conn.cursor()
        try:        
            c.execute(''' DROP TABLE tweets''')
        except Exception as ex:
            print(ex)

        table_sql = """
            CREATE TABLE tweets (
                id integer NOT NULL,
                author_id integer NOT NULL,
                tweet_text text NOT NULL,
                created_at text NOT NULL,
                PRIMARY KEY (id, author_id))
            """
        c.execute(table_sql)
        self.conn.commit()

    def reset_processed_tweets(self):
        c = self.conn.cursor()
        try:                    
            c.execute('''DROP TABLE processed_tweets''')
            self.conn.commit()
        except Exception as ex:
            print(ex)
        table_sql = '''
            CREATE TABLE processed_tweets (
                tweet_id text NOT NULL,
                tag text NOT NULL,
                token text NOT NULL
                );
            '''

        c.execute(table_sql)
        self.conn.commit()

    def tweets_to_tuple_list(self, tweets):
        return [(   x['id'],
                    x['author_id'],
                    x['text'],
                    x['created_at']) for x in tweets]

    def save_tweets(self, tweets):
        tupled_tweets = self.tweets_to_tuple_list(tweets)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO tweets VALUES(?, ?, ?, ?)", tupled_tweets)

        self.conn.commit()

    def tweets(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM tweets")
        for (tweet,) in c:
            yield tweet

    def remove_URL(self, sample):
        """Remove URLs from a sample string"""
        return re.sub(r"http\S+", "", sample)

    def get_tweet_texts(self):
        c = self.conn.cursor()
        c.execute("SELECT id, tweet_text FROM tweets")
        for (tweet_id, tweet_text) in c:
            yield (tweet_id, self.remove_URL(tweet_text))

    def save_processed_tweets(self, tagged_sent_gen):
        c = self.conn.cursor()

        for sent in tagged_sent_gen:
            c.executemany('''
                INSERT OR IGNORE 
                INTO processed_tweets (tweet_id, token, tag) 
                VALUES(?, ?, ?)
                '''
                , sent)

        self.conn.commit()

    def get_processed_tweets(self):
        c = self.conn.cursor()
        c.execute('SELECT DISTINCT tweet_id FROM processed_tweets')
        tweet_list = c.fetchall()
        for (tweet_id,) in tweet_list:
            c.execute('''SELECT token, tag FROM processed_tweets
                WHERE tweet_id=?''', (tweet_id,))
            tweet_tokens = c.fetchall()
            yield tweet_tokens

    def get_processed_tokens(self):
        for processed_tweet in self.get_processed_tweets():
            yield [token for (token, tag) in processed_tweet]

    def get_tweets_vocabulary(self):
        c = self.conn.cursor()
        c.execute('''SELECT DISTINCT token FROM processed_tweets
                ORDER BY token ASC''')
        return [token for (token,) in c.fetchall()]
        
























