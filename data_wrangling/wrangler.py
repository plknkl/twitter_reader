from nltk import sent_tokenize, pos_tag, download, FreqDist
from nltk.tokenize import TweetTokenizer
import itertools
import time


class Wrangler:

    def __init__(self, tweet_gen):
        # tweet_gen contains (id, tweet_text)
        try:
            self.tweet_gen = map(lambda x: self.sent_gen(x), tweet_gen)
        except LookupError:
            download('averaged_perceptron_tagger')
            self.tweet_gen = map(lambda x: self.sent_gen(x), tweet_gen)

    def explicit_filter(self, token):
        # to be extracted into json
        bad_tokens = ['RT']
        if token in bad_tokens:
            return False
        else:
            return True

    def sent_gen(self, tweet):
        tweet_id, tweet_text = tweet
        for sent in sent_tokenize(tweet_text):
            tag_list = pos_tag(self.word_list(sent))
            id_tag_list = []
            for token_tag in tag_list:
                id_tag_list.append((tweet_id, token_tag[0], token_tag[1]))
            yield id_tag_list

    def word_list(self, sentence):
        tweet_tokenizer = TweetTokenizer()
        return list(filter(self.explicit_filter, tweet_tokenizer.tokenize(sentence)))

    def tokenize(self):
        # main method for wrangle data
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

        
