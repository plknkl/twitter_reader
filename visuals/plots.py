from wordcloud import WordCloud

def wordcloud(sentence_list):
    long_string = ','.join(sentence_list)

    wordcloud = WordCloud(
        background_color='white', 
        max_words=5000, 
        contour_width=3,
        width=1024,
        height=768,
        contour_color='steelblue')

    wordcloud.generate(long_string)

    return wordcloud.to_image()
