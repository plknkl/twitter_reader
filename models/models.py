import nltk
from nltk.cluster import KMeansClusterer
from sklearn.base import BaseEstimator, TransformerMixin

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
