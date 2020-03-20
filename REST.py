from pymongo import MongoClient
import tweepy
import credentials
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
import re
import plotly.express as px
import pandas as pd

#Authenticating
auth = tweepy.AppAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

#Initialise the Mongodb
mongo_client = MongoClient()
db = mongo_client.twitterdb
col = db.tweet_storage

#Appending the tweets into the list with the keyword extended_tweet and text
ln = []
for doc in col.find({}):
    if 'extended_tweet' in doc:
        ln.append(doc['extended_tweet']['full_text'])
    elif 'text' in doc:
        ln.append(doc['text'])

#Strip off all the unncessary keywords and punctuations using regular expressions
content = ' '.join(ln)
content = re.sub(r"http\S+", "", content)
content = content.replace('RT ', ' ').replace('&amp;', 'and')
content = re.sub('[^A-Za-z0-9]+', ' ', content)
content = content.lower()
tokenized = word_tokenize(content)

#Filter out the stop words and append to a new list
stop_words=set(stopwords.words("english"))
stop_words.add('u')
stop_words.add('like')
stop_words.add('ur')
filtered=[]
for w in tokenized:
    if w not in stop_words:
        if (w.isnumeric() == False):
            filtered.append(w)

#Find the frequency of the top 50 most common words
fdist = FreqDist(filtered)
fd = pd.DataFrame(fdist.most_common(50), columns = ["Topic","Frequency"]).reindex()

#Plot the results
fig = px.bar(fd, x="Topic", y="Frequency")
fig.update_traces(marker_line_width=1.5)
fig.show()

#Do a RESTapi search on the most common topic
keyword = fd.Topic[0]
for status in tweepy.Cursor(api.search, q=keyword, lang="en", include_entities=True, tweet_mode='extended').items(100000):
	db.tweets_RESTapi.insert(status._json)
