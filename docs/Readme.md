# Twitter Explorer

This tool is used to gather information from free Twitter API which lets you query the last 7 days of Twitter activity (some throtteling might apply on API requests).

There are several modules involved in gathering and analysing the text data with Natural Language Processing (NLP) and Machine Learning techniques.

#### Data Gathering

The first module is called _data_access.twitter_reader_ containing _TwitterReader_ class.
To instantiante the object one should provide an _api_key.json_ object (obtained from Twitter) formatted as follows:

```
{
  "api": "_api_key_",
  "api_secret": "_api_secret_key_",
  "bearer": "_bearer_token_"
}
```

Once the _TwitterReader_ is instantiated a meaningful request query should be loaded. 
A dictionary is needed to create a meaningful query 
something like `query_dict = {'#': ['NYC', 'Happy'], 'keyword': ['cold', 'winter']}`
with hashtags in OR logic, and keywords in AND logic.

Once the desired dictionary is created, it can be loaded using `twitterReader.set_query(query_dict)`.

At this point one could send the request to the Twitter API using the `twitterReader.read(pages=10)` method, which returns a list of tweets. The _pages_ option controls the amount of pages read, since twitter paginates the request results in chunks of 100 tweets per page.

Result example:

```
[{'created_at': '2020-12-21T07:43:48.000Z',
  'id': '1340925924888469510',
  'text': '#winter #happy #season #snow #storm #rainy #snowy #cloudy #heater #cold #snowman #ski #life #lifestyle #wealthy #healthy #enjoy #interested #attractive #fire https://t.co/aLYWYjsm99',
  'author_id': '2152766298'},
  
 {'created_at': '2020-12-20T20:54:39.000Z',
  'id': '1340762560883245058',
  'text': 'I suspect that the old neighborhood looks something like this, today.\n.\n.\n#winter #winterwonderland #wintertime #queens #newyorkcity #nyc #newyork #snow #snowfall #snowscape #cold #coldweather #buried @ Queens, New York https://t.co/dUvSY4xej7',
  'author_id': '334741860'},
  
 {'created_at': '2020-12-20T12:00:01.000Z',
  'id': '1340628017291407363',
  'text': 'Energy Audit: Lower Energy Bill. https://t.co/6lOOiJYBOs Call: (256) 656-7654. #energy #audit #cold #lower #your #energy #bill #savings #money #energyservices #happy #winter #December #budget2020 #energycostsavings #huntsvillealabama #retconenergy #changeyourenergystory https://t.co/jjLUQG0PxW',
  'author_id': '793681461450829825'}]
```

#### Data Storage

Once read from Twitter API the data should be stored in a persistent way, since the trial and error of the analysis requires multiple reads for trying out different approaches. The _DBManager_ from _data_storage.db_manager_ uses an underlying sqlite database for that purpose. Once we obtain our _list_of_tweets_ from the _TwitterReader_ we can use `db_manager.save_tweets(list_of_tweets)` for saving our list of raw tweets to the database.

#### Wrangler

Now that we have our raw data saved to the database, we need to preprocess the data, before proceeding to further analysis. The whole transformation pipeline is based on python generators so precise steps are required. First we pull the data from the database with _db_manager_ which was already lightly processed. From `db_manager.get_tweet_texts()` we will obtain a generator of tweets, striped from the eventual urls present into them.
Every tweet will be a tuple of _(tweet_id, tweet_text)_ something like:

```
(1340628017291407363,
 'Energy Audit: Lower Energy Bill.  Call: (256) 656-7654. #energy #audit #cold #lower #your #energy #bill #savings #money #energyservices #happy #winter #December #budget2020 #energycostsavings #huntsvillealabama #retconenergy #changeyourenergystory')
```

  Time to feed those tweet tuples to a _data_wrangling.wrangler.Wrangler_, passing the generator to the constructor, like:
  `wrangler = Wrangler(db_manager.get_tweet_texts())`

  Now that our wrangler have a feeding point, we can call `processed_tweets = wrangler.tokenize()` on it. The _tokenize_ method will perform several transformations on our loaded tweet, returning a token generator. First it will split our tweet into sentences. For every sentence it will then tokenize the words, creating a sentence list where every list element is a tuple of _(tweet_id, word, pos_tag)_. Part of speech tagging _(pos_tag)_ let us retain the information regarding the grammatical structure of the sentence, for example _NNP_ meaning proper noun, singular ‘Bill’. An example of a single sentence item returned by the _tokenize()_ method:

  ```
  [(1340628017291407363, 'Energy', 'NNP'),
 (1340628017291407363, 'Audit', 'NNP'),
 (1340628017291407363, ':', ':'),
 (1340628017291407363, 'Lower', 'NNP'),
 (1340628017291407363, 'Energy', 'NNP'),
 (1340628017291407363, 'Bill', 'NNP'),
 (1340628017291407363, '.', '.')]
  ```

 Now that we have split our tweets into sentences, striped from urls, and tagged every sentence words with _pos_tag_, we can save again our preprocessed material with `db_manager.save_processed_tweets(processed_tweets)`. 

#### Text Normalizaton

There is one more step which is made before feeding our data to the analysis algorithms, where we will filter out all the stop words, punctuation, and will lemmatize our words. The lemmatization process consist in reducing the words to their base form. For example, in English, the verb 'to walk' may appear as 'walk', 'walked', 'walks' or 'walking'. The base form, 'walk', that one might look up in a dictionary, is called the lemma for the word. This way our algorhitms will have fewer information entropy to deal with. 
A sentence like:
_'I suspect that the old neighborhood looks something like this, today.'_
will turn into:
_'suspect old neighborhood look something like today'_.

After instantiating our normalization object with `text_normalizer = TextNormalizer()` we get our processed tweets with `processed_tweets = db_manager.get_processed_tweets()`, normalizing finally with `transformed_text = text_normalizer.transform(processed_tweets)`. Now our _transformed_text_ variable is holding in memory the whole normalized tweets list, like:

```
['#winter #happy #season #snow #storm #rainy #snowy #cloudy #heater #cold #snowman #ski #life #lifestyle #wealthy #healthy #enjoy #interested #attractive #fire',

 'suspect old neighborhood look something like today #winter #winterwonderland #wintertime #queens #newyorkcity #nyc #newyork #snow #snowfall #snowscape #cold #coldweather #buried queens new york',
 
 'energy audit lower energy bill call (256) 656-7654 #energy #audit #cold #lower #your #energy #bill #savings #money #energyservices #happy #winter #december #budget2020 #energycostsavings #huntsvillealabama #retconenergy #changeyourenergystory']
```

## Visual Functions

There are few functions which we can invoke in order to help us with our _Twitter Exploration_. Words frequency distribution, Word Cloud and Clustering are implemented.

#### Frequency Distribution

This function gives us a horizontal bar chart with the frequency of every word in our tweets set.

_visuals.plots.frequency_distribution(transformed_text)_ gives us just that.![](/home/nikolai/Projects/twitter-nlp-notebook/docs/pics/frequency_distribution.svg)

#### Word Cloud

The _visuals.plots.wordcloud(transformed_text)_ creates an image where the top 20 words are visualized with their relative proportional size.



<img src="/home/nikolai/Projects/twitter-nlp-notebook/docs/pics/wordcloud.png" style="zoom:50%;" />



#### Clustering

A general data overview could be made with the function _visuals.plots.t_sne(transformed_text)_ . This function performs a t-Distributed Stochastic Neighbor Embedding, a non-linear technique for dimensionality reduction. Our tweets originally are in a n-dimentional space where n is equal to the corpus vocabulary (set of all words distinct words), and every tweet word being the coordinate in that space. The dimensionality reduction is necessary to visually represent our tweets in a bidimentional space. This probabilistic approach gives us a graphical representation as follows, even though we loose the point/tweet mapping, so it is usefull only as a plotting technique.

![](/home/nikolai/Projects/twitter-nlp-notebook/docs/pics/tsne.svg)

What we can do is to use the classical K-means clustering technique to find tweet/cluster mappings and later visualize the output clustres with the former t-sne analysis to evaluate the relative fitness of the K-means clustering. First we will instantiate a _models.models.Cluster_ object, with 3 clusters, and next we'll use the function _Cluster.clustered_text_ to receive a list of tuples  _(text, cluster)_.

```
cluster = Cluster(k=3)
clustered_text = cluster.clustered_text(transformed_text)
```

Once we obtain our _clustered_text_ we can pass that to the t-sne function with which will color the points based on relative clusters.

```
t_sne_clustered(clustered_text)
```

![](/home/nikolai/Projects/twitter-nlp-notebook/docs/pics/tsne2.svg)

From this plot we can see that clusters 1 and 2 have some distance, where cluster 0 is a sort of middle ground in between. 



### Topic Understanding

The final function which we can use is a topic extractor, from _models.models.get_relevant_topic_ . This function uses _latent Dirichlet allocation_, a Bayesian probabilistic model, finding the most significant words from a sentence list. 

After some text extraction with _data_transformers.extractors.text_from_cluster_ we feed the function the sentences from cluster 1, obtaining the following topic words:

```
cluster_one = text_from_cluster(clustered_text, 1)
get_relevant_topic(cluster_one)
-------
['wet', 'dip', 'evening', '31', 'brisk']
```

Feeding the function the sentences from cluster 2 we will obtain the following topic words:

```
cluster_two = text_from_cluster(clustered_text, 2)
get_relevant_topic(cluster_two)
-------
['december', 'your', 'new', 'happy', 'winter']
```



Thus, we can see that the former cluster is about the weather, where the latter is about holidays.



There are some handy extractors for further manual analysis, like 

* _data_transformers.extractors.ids_from_cluster_

* _data_storage.db_manager.urls_fom_ids_

    

The first one lets us extract the tweet ids from _clustered_text_, and the other retreives all the urls (if present) from the contents of those tweets. With this operation we can obtain several urls if we need further exploration of a certain cluster. 

```
ids = ids_from_cluster(clustered_text, 1)
db_manager.get_tweet_urls(tweet_ids=ids)
```



For the weather cluster we obtain a link which gets us here:

<img src="/home/nikolai/Pictures/Screenshot from 2020-12-22 16-22-09.png" style="zoom: 33%;" />



For the holiday cluster  we obtain another link which gets us there:

<img src="/home/nikolai/Pictures/Screenshot from 2020-12-22 16-31-18.png" style="zoom:33%;" />



Twitter Explorer aims to be a handy little tool in the hands of a data analyst for understanding what are people really talking about on Twitter, following little information bits like hashtags and keywords. 