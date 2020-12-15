import unicodedata
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

class TextNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self, language='english'):
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words(language))

    def is_stopword(self, token):
        return token.lower() in self.stopwords

    def lemmatize(self, token, pos_tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ

        }.get(pos_tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

    def normalize(self, tweet):
        return [
            self.lemmatize(token, tag).lower()
            for (token, tag) in tweet
            if not self.is_stopword(token)
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, tweet_gen):
        return [' '.join(self.normalize(tweet)) for tweet in tweet_gen]
