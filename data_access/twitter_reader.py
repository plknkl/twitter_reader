import requests
import os
import json
from urllib.parse import quote_plus

class TwitterReader:

    def __init__(self, conf_json_path):
        self.conf_json_path = conf_json_path
        self.query = None
        self.page_tracking = 0

    def auth(self):
        with open(self.conf_json_path) as f:
            data = json.load(f)
        return data['bearer']

    # A dictionary is needed to create a meaningful query
    # something like query_dict = {'#': ['Roma', 'Milano'], 'keyword': ['freddo']}
    # with hashtags in OR logic, and keywords in AND logic
    def set_query(self, query_dict):
        dic = query_dict
        q = ''
        for key in dic.keys():
            if key == 'keyword':
                q += ' '.join(dic[key])
            if key == '#':
                tag_list = list(map(lambda x: '#'+x, dic[key]))
                q += '(%s)' % (' OR '.join(tag_list))
        self.query = quote_plus(q)


    def create_url(self, next_token=None):
        
        if self.query == None:
            print('''missing query, please add a query 
                with set_query method''')
            return None

        query = self.query
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        tweet_fields = "tweet.fields=author_id,text,created_at"
        options = "max_results=100"
        if next_token == None:
            url = ('https://api.twitter.com/2/tweets/search/'
                f'recent?query={query}&{options}&{tweet_fields}')
        else:
            url = ('https://api.twitter.com/2/tweets/search/'
                f'recent?query={query}&next_token={next_token}&{options}&{tweet_fields}')
        # print(url)
        return url


    def create_headers(self, bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers


    def connect_to_endpoint(self, url, headers):
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            self.page_tracking += 1
            print(f'page {self.page_tracking}...ok')
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()


    def read(self, pages=1):
        bearer_token = self.auth()
        response_list = []

        # given with the first request for getting
        # next pages
        next_token = None
        
        for i in range(pages):
            url = self.create_url(next_token)
            if url:
                headers = self.create_headers(bearer_token)
                json_response = self.connect_to_endpoint(url, headers)
                next_token = json_response['meta']['next_token']
                response_list += json_response['data']
                if len(next_token) < 3:
                    print('no more tweets available')
                    return response_list
            else:
                return None
        self.page_tracking += 0
        print(f'{len(response_list)} tweets read.')
        return response_list

