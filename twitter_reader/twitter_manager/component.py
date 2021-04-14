import requests
import os
import json


class APIConfig:
    def __init__(self, conf_json_path='./local_configs/api_keys.json', lang=None):
        self.conf_json_path = conf_json_path
        with open(self.conf_json_path) as f:
            data = json.load(f)
        self.bearer = data['bearer']
        self.tweet_fields = ['author_id','text','created_at']
        self.options = {'max_results': 10}

class APIManager:
    def __init__(self, config: APIConfig):
        self.config = config

    def query(self, query: str, pages=1):
        """A simple query which gives back Tweets"""
        tweets = []
        headers = {"Authorization": "Bearer {}".format(self.config.bearer)}
        options = self._stringify_options(self.config.options)
        tweet_fields = 'tweet.fields='+','.join(self.config.tweet_fields)
        
        next_token = None
        for page in range(pages):
            if not next_token:
                url = ('https://api.twitter.com/2/tweets/search/'
                        f'recent?query={query}&{options}&{tweet_fields}')
                json_response = self._connect_to_endpoint(url, headers)
            else:
                url = ('https://api.twitter.com/2/tweets/search/'
                        f'recent?query={query}&next_token={next_token}&{options}&{tweet_fields}')
                json_response = self._connect_to_endpoint(url, headers)
            tweets += json_response['data']
            if 'next_token' in json_response['meta'].keys():
                next_token = json_response['meta']['next_token']
            else:
                break
        return tweets

    def _stringify_options(self, options:{}) -> str:
        options_str = ''
        for k in options.keys():
            options_str += f'{k}={options[k]}'
        return options_str

    def _connect_to_endpoint(self, url, headers):
        response = requests.request("GET", url, headers=headers)
        json_response = None
        if response.status_code == 200:
            json_response = response.json()
            response_data_len = len(json_response['data'])
            print(f'got {response_data_len} tweets.')
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return json_response


# class TwitterReader:

#     def __init__(self, conf_json_path='./local_configs/api_keys.json', lang=None):
#         self.conf_json_path = conf_json_path
#         self.query = None
#         self.lang = lang
#         self.page_tracking = 0

#     def _auth(self):
#         with open(self.conf_json_path) as f:
#             data = json.load(f)
#         return data['bearer']

#     def create_search_url(self, next_token=None):
        
#         if self.query == None:
#             print('''missing query, please add a query 
#                 with set_query method''')
#             return None

#         query = self.query
#         # Tweet fields are adjustable.
#         # Options include:
#         # attachments, author_id, context_annotations,
#         # conversation_id, created_at, entities, geo, id,
#         # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
#         # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
#         # source, text, and withheld
#         tweet_fields = "tweet.fields=author_id,text,created_at"
#         options = "max_results=10"
#         if next_token == None:
#             url = ('https://api.twitter.com/2/tweets/search/'
#                 f'recent?query={query}&{options}&{tweet_fields}')
#         else:
#             url = ('https://api.twitter.com/2/tweets/search/'
#                 f'recent?query={query}&next_token={next_token}&{options}&{tweet_fields}')
#         print(url)
#         return url

#     # def create_headers(self, bearer_token):
#     #     headers = {"Authorization": "Bearer {}".format(bearer_token)}
#     #     return headers


#     def read(self, url, pages=1):
#         bearer_token = self._auth()
#         response_list = []
        
#         for i in range(pages):
#             if url:
#                 headers = self.create_headers(bearer_token)
#                 json_response = self.connect_to_endpoint(url, headers)
#                 if 'meta' in json_response.keys():
#                     if json_response['meta']['result_count'] == 0:
#                         print('no more tweets available')
#                         return response_list

#                     if 'next_token' in json_response['meta'].keys():
#                         next_token = json_response['meta']['next_token']
#                     else:
#                         next_token = None
#                     response_list += json_response['data']
#                     if not next_token:
#                         print('no more tweets available')
#                         return response_list
#                 else:
#                     return json_response
#             else:
#                 return None
#         self.page_tracking += 0
#         print(f'{len(response_list)} tweets read.')
#         return response_list

#     def search(self, query):
#         self.query = query
#         # given with the first request for getting
#         # next pages
#         next_token = None
#         url = self.create_search_url(next_token)
#         return self.read(url)

#     def get_tweet(self, id):
#         tweet_fields = "tweet.fields=author_id,text,created_at,conversation_id"
#         url = ('https://api.twitter.com/2/tweets?'
#                 f'ids={id}&{tweet_fields}')
#         return self.read(url)
