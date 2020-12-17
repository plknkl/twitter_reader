from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer

class OneHotVectorizer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.vectorizer = CountVectorizer(binary=True)

    def fit(self, tweet_gen, labels=None):
        return self

    def transform(self, tweets):
        freqs = self.vectorizer.fit_transform(tweets)
        return [freq.toarray()[0] for freq in freqs]

