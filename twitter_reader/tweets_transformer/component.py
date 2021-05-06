import re

def de_emojify(text: str):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def text_only(tweet_text: str):
    # remove emoji
    tweet_text = de_emojify(tweet_text)
    # remove retweet tag
    pattern = '^RT\s@.*:\s'
    tweet_text = re.sub(pattern, '', tweet_text)
    # remove \n
    tweet_text = re.sub('\\n', ' ', tweet_text)
    # remove single tags
    tweet_text = re.sub('\$|#', '', tweet_text)
    # remove double spaces
    tweet_text = re.sub('\s+', ' ', tweet_text)
    # remove user references 
    tweet_text = re.sub('@\w+', '', tweet_text)
    # remove web link 
    tweet_text = re.sub('http.*\S', '', tweet_text)
    # strip
    tweet_text = tweet_text.strip()
    
    return tweet_text
