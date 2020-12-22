from wordcloud import WordCloud
from data_transformers.normalizers import TextNormalizer 
from yellowbrick.text.freqdist import FrequencyVisualizer
from sklearn.feature_extraction.text import CountVectorizer
from yellowbrick.text import TSNEVisualizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt

def strip_twitter_ids(transformed_text):
    return [text for text, tweet_id in transformed_text]

def wordcloud(transformed_text):
    transformed_text = strip_twitter_ids(transformed_text)
    long_string = ','.join(transformed_text)

    wordcloud = WordCloud(
        background_color='white', 
        max_words=20, 
        contour_width=3,
        width=1024,
        height=768,
        contour_color='steelblue')

    wordcloud.generate(long_string)

    return wordcloud.to_image()

def frequency_distribution(transformed_text):
    transformed_text = strip_twitter_ids(transformed_text)
    plt.tick_params(labelsize=8)
    vectorizer = CountVectorizer()
    docs = vectorizer.fit_transform(transformed_text)
    features = vectorizer.get_feature_names()
    visualizer = FrequencyVisualizer(features=features, size=(1080, 720))
    visualizer.fit(docs)
    return visualizer

def t_sne(transformed_text):
    transformed_text, tweets_ids = list(zip(*transformed_text))
    tfidf = TfidfVectorizer()
    docs = tfidf.fit_transform(transformed_text)
    tsne = TSNEVisualizer(colors=[
        ('#f7aa00'),('#235784'),('#40a8c4'),('#bcdbdf'),('#c6fced')
    ])

    tsne.fit(docs)
    return tsne.finalize()

def t_sne_clustered(transformed_text):
    transformed_text, tweets_ids = list(zip(*transformed_text))
    transformed_text, cluster_list = list(zip(*transformed_text))
    tfidf = TfidfVectorizer()
    docs = tfidf.fit_transform(transformed_text)
    tsne = TSNEVisualizer(colors=[
        ('#f7aa00'),('#235784'),('#40a8c4'),('#bcdbdf'),('#c6fced')
    ])

    tsne.fit(docs, cluster_list)
    return tsne.finalize()
