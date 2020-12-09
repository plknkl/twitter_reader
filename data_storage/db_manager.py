import sqlite3
import re

def connect():
    conn = sqlite3.connect('./db/db.sqlite3')
    return conn

def create_table_if_needed():
    conn = connect()
    c = conn.cursor()
			
    #get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master
                WHERE type='table' AND name='tweets' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 :
        print('Table exists.')
    else:
        print('Table needed.')
        table_sql = """
            CREATE TABLE tweets (
                id integer,
                author_id integer NOT NULL,
                tweet_text text NOT NULL,
                created_at text NOT NULL,
                PRIMARY KEY (id, author_id))
            """

        c.execute(table_sql)
        print('Table created.')
                
    #commit the changes to db			
    conn.commit()

    return conn

def tweets_to_tuple_list(tweets):
    return [(   x['id'],
                x['author_id'],
                x['text'],
                x['created_at']) for x in tweets]

def save_tweets(tweets):
    # returns connection so it can be reused
    conn = create_table_if_needed()
    with conn:
        tupled_tweets = tweets_to_tuple_list(tweets)
        cur = conn.cursor()
        cur.executemany("INSERT OR IGNORE INTO tweets VALUES(?, ?, ?, ?)", tupled_tweets)
        #commit the changes to db			
        conn.commit()

def tweets():
    conn = connect()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tweets")
        for tweet in iter(cur.fetchone, None):
            yield tweet

def remove_URL(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", sample)

def texts():
    conn = connect()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT tweet_text FROM tweets")
        for text in iter(cur.fetchone, None):
            yield remove_URL(text[0])

























