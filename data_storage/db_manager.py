import sqlite3
import re

def connect():
    conn = sqlite3.connect('./db/db.sqlite3')
    return conn

def reset_db():
    conn = connect()
    c = conn.cursor()
			
    #get the count of tables with the name
    c.execute(''' DROP TABLE tweets''')
    conn.commit()
    conn.close

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
        c = conn.cursor()
        c.executemany("INSERT OR IGNORE INTO tweets VALUES(?, ?, ?, ?)", tupled_tweets)
        #commit the changes to db			
        conn.commit()

def tweets():
    conn = connect()
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tweets")
        for tweet in iter(c.fetchone, None):
            yield tweet

def remove_URL(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", sample)

def tweet_texts():
    conn = connect()
    with conn:
        c = conn.cursor()
        c.execute("SELECT tweet_text FROM tweets")
        for text in iter(c.fetchone, None):
            yield remove_URL(text[0])

def save_processed_tweets(tagged_sent_gen):
    conn = connect()
    with conn:
        c = conn.cursor()

        try:
            c.execute(''' DROP TABLE processed_tweets''')
        except:
            print('table not found')

        table_sql = '''
            CREATE TABLE processed_tweets (
                tag text NOT NULL,
                token text NOT NULL
                );
            '''

        c.execute(table_sql)

        for sent in tagged_sent_gen:
            c.executemany('''
                INSERT OR IGNORE 
                INTO processed_tweets (token, tag) 
                VALUES(?, ?)
                '''
                , sent)


def get_processed_tweets():
    conn = connect()
    with conn:
        c = conn.cursor()
        c.execute("SELECT token, tag FROM processed_tweets")
        for token in iter(c.fetchone, None):
            yield token
























