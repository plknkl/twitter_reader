import nltk
from nltk.cluster import KMeansClusterer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from data_transformers.normalizers import TextNormalizer 
from data_transformers.vectorizer import OneHotVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def get_relevant_topic(sentence_list, topic_length=5):
    n_topics = 1
    model = Pipeline([
        ('vect', OneHotVectorizer()),
        ('model', LatentDirichletAllocation(n_components=n_topics)),
    ])
    

    result = []
    model.fit_transform(sentence_list)
    words = model['vect'].vectorizer.get_feature_names()

    for topic_idx, topic in enumerate(model['model'].components_):
        result += [words[i] for i in topic.argsort()[-topic_length-1:-1]]
    return result


class KMeansClusters(BaseEstimator, TransformerMixin):

    def __init__(self, k=2):
        """
        k is the number of clusters
        model is the implementation of Kmeans
        """
        self.k = k
        self.distance = nltk.cluster.util.cosine_distance
        self.model = KMeansClusterer(self.k, self.distance,
                                     avoid_empty_clusters=True)

    
    def fit(self, tweets, labels=None):
        return self

    def transform(self, tweets):
        """
        Fits the K-means model to one-hot vectorized documents.
        """
        return self.model.cluster(tweets, assign_clusters=True)

class Cluster:

    def __init__(self, k=2):
        self.k = k

    def clustered_text(self, transformed_text):
        (transformed_text, tweet_ids) = list(zip(*transformed_text))
        model = Pipeline([
            ('vect', OneHotVectorizer()),
            ('clusters', KMeansClusters(k=self.k))
        ])
       
        result = {}
        clusters = model.fit_transform(transformed_text)

        clustered_text = list(zip(transformed_text, clusters))

        return list(zip(clustered_text, tweet_ids))















