from wordcloud import WordCloud
from data_transformers.normalizers import TextNormalizer 
from yellowbrick.text.freqdist import FrequencyVisualizer
from sklearn.feature_extraction.text import CountVectorizer
from yellowbrick.text import TSNEVisualizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt


def wordcloud(sentence_list):
    long_string = ','.join(sentence_list)

    wordcloud = WordCloud(
        background_color='white', 
        max_words=20, 
        contour_width=3,
        width=1024,
        height=768,
        contour_color='steelblue')

    wordcloud.generate(long_string)

    return wordcloud.to_image()

def frequency_distribution(sentence_list):
    plt.tick_params(labelsize=8)
    vectorizer = CountVectorizer()
    docs = vectorizer.fit_transform(sentence_list)
    features = vectorizer.get_feature_names()
    visualizer = FrequencyVisualizer(features=features, size=(1080, 720))
    visualizer.fit(docs)
    return visualizer

def t_sne(sentence_list, cluster_list=None):
    tfidf = TfidfVectorizer()
    docs = tfidf.fit_transform(sentence_list)
    tsne = TSNEVisualizer(colors=[
        ('#f7aa00'),('#235784'),('#40a8c4'),('#bcdbdf'),('#c6fced')
    ])

    tsne.fit(docs, cluster_list)
    return tsne
