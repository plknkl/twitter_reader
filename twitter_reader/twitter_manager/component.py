import requests
import os
import json
import urllib

class Tweet:
    def __init__(self, raw_tweet_dict):
        self.id = raw_tweet_dict['id']
        self.text = raw_tweet_dict['text']
        self.raw = raw_tweet_dict

class APIConfig:
    def __init__(self, conf_json_path='./local_configs/api_keys.json', lang=None):
        self.conf_json_path = conf_json_path
        with open(self.conf_json_path) as f:
            data = json.load(f)
        self.bearer = data['bearer']
        self.tweet_fields = ['text']
        self.options = {'max_results': 10,
                        'expansions': 'referenced_tweets.id'}

class APIManager:
    def __init__(self, config: APIConfig):
        self.config = config
        self.found_tweets = []

    def query(self, query: str, pages=1):
        """A simple query which gives back Tweets"""
        query = urllib.parse.quote(query)
        result_list = []
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
            result_list.append(json_response)
            if 'next_token' in json_response['meta'].keys():
                next_token = json_response['meta']['next_token']
            else:
                break
        tweets = self._extract_tweets(result_list)
        self.found_tweets = [Tweet(t) for t in tweets]
        return self.found_tweets

    def _extract_tweets(self, query_result_list):
        tweets = []
        for page in query_result_list:
            tweets += page['data']
        return tweets

    def _stringify_options(self, options:{}) -> str:
        options_list = []
        for k in options.keys():
            options_list.append(f'{k}={options[k]}')
        return '&'.join(options_list)

    def _connect_to_endpoint(self, url, headers):
        print(url)
        print('--')
        response = requests.request("GET", url, headers=headers)
        json_response = None
        if response.status_code == 200:
            json_response = response.json()
            response_data_len = len(json_response['data'])
            print(f'got {response_data_len} tweets.')
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return json_response
