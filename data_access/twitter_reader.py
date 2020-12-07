import requests
import os
import json
from urllib.parse import quote_plus

class TwitterReader:

    def __init__(self, conf_json_path):
        self.conf_json_path = conf_json_path

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


    def create_url(self):
        query = self.query
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        tweet_fields = "tweet.fields=author_id,text,created_at"
        url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&{tweet_fields}'
        return url


    def create_headers(self, bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers


    def connect_to_endpoint(self, url, headers):
        response = requests.request("GET", url, headers=headers)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()


    def read(self):
        bearer_token = self.auth()
        url = self.create_url()
        headers = self.create_headers(bearer_token)
        json_response = self.connect_to_endpoint(url, headers)
        return json_response

