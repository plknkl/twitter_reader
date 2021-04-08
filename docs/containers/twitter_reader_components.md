```mermaid
graph TD
    jupyter[Jupyter Notebook] -->|imports| data_storage[Data Storage]
    jupyter -->|imports| twitter_manager[Twitter Manager]
    data_storage -->|rw| database[Database]
    twitter_manager[Twitter Manager] -->|queries| twitter_api[Twitter Api]
```

## Components

### Jupyter Notebook
The notebook is used as the interface for the user, it imports the Twitter Manager component for querying the Twitter API, and imports the Data Storage module to have some persistance.
***
### Twitter Manager
Can query the Twitter API with a term.
<br>
<br>
```python
query(query: str, config: APIConfig, pages=1):
    """A simple query which gives back Tweets"""
```
Given a twitter query, this function pulls back a list of tweets in dictionary format.
One can ask for a certain number of pages to be retrieved. The tweets per page are defined in the APIConfig model (_max results_ parameter).
***
### Data Storage
Can save and read saved tweets.
<br>
<br>
```python
save_tweets(tweets: [], config) -> None:
    """A function which pushes tweet dicts to a db"""
```
Saves a list of tweets, which are just a list of dictionaries.
<br>
<br>
```python
read_tweets(config: DBConfig) -> []:
    """A function which pulls all tweet dicts from a db"""
```
Reads a list of tweets from the database table.
<br>
<br>
```python
clear_tweet_table(config: DBConfig) -> None:
    """A function which clears the tweet table"""
```
Clears all previously stored tweets.
<div style="page-break-after: always;"></div>



## Models

### DBConfig
A model for storing the database configuration
```python
dbname='twitter'
host='localhost'
user='postgres'
password='bobolo'
```


### APIConfig
A model for storing twitter api configuration
```python
conf_json_path = './local_configs/api_keys.json'
bearer = 'aaaaabbbbbbbcccc'
tweet_fields = ['author_id','text','created_at']
options = {'max_results': 10}
```