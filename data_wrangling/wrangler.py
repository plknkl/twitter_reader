from nltk import sent_tokenize, pos_tag, download, FreqDist
from nltk.tokenize import TweetTokenizer
import itertools
import time


class Wrangler:

    def __init__(self, tweet_gen):
        try:
            self.tweet_gen = map(lambda x: self.sent_gen(x), tweet_gen)
        except LookupError:
            download('averaged_perceptron_tagger')
            self.tweet_gen = map(lambda x: self.sent_gen(x), tweet_gen)

    def sent_gen(self, tweet):
        for sent in sent_tokenize(tweet):
            yield pos_tag(self.word_list(sent))

    def word_list(self, sentence):
        tweet_tokenizer = TweetTokenizer()
        return tweet_tokenizer.tokenize(sentence)

    def tokenize(self):
        # Perform single pass over tweets, tokenize and count
        for tweet in self.tweet_gen:
            for sent in tweet:
                yield sent

    def describe(self):
        """ Performs a single pass of the corpus and
            returns a dictionary with a variety of metrics
            concerning the state of the corpus.
        """
        
        started = time.time()

        # Structures to perform counting.
        counts = FreqDist()
        tokens = FreqDist()

        # Perform single pass over tweets, tokenize and count
        for tweet in self.tweet_gen:
            counts['tweets'] += 1

            for sent in tweet:
                counts['sents'] += 1

                for word, tag in sent:
                    counts['words'] += 1
                    tokens[word] += 1
    
        return {
            'tweets': counts['tweets'],
            'sents':  counts['sents'],
            'words':  counts['words'],
            'vocab':  len(tokens),
            'secs':   round(time.time() - started)
        }

        
