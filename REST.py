from pymongo import MongoClient
import tweepy
import argparse
import configparser
import json
import credentials
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
import re
import plotly.express as px
import pandas as pd
import crawler
import sys
import jsonpickle
import os
import credentials


auth = tweepy.AppAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

mongo_client = MongoClient()
db = mongo_client.twitterdb
col = db.tweet_storage

ln = []

for doc in col.find({}):
    if 'extended_tweet' in doc:
        ln.append(doc['extended_tweet']['full_text'])
    elif 'text' in doc:
        ln.append(doc['text'])

content = ' '.join(ln)
content = re.sub(r"http\S+", "", content)
content = content.replace('RT ', ' ').replace('&amp;', 'and')
content = re.sub('[^A-Za-z0-9]+', ' ', content)
content = content.lower()
tokenized = word_tokenize(content)

'''
content2 = ' '.join(ln)
content2 = re.sub(r"http\S+", "", content2)
content2 = content2.replace('RT ', ' ').replace('&amp;', 'and')
content2 = re.sub('[^A-Za-z0-9#]+', ' ', content2)
content2 = content2.lower()
tknzr = TweetTokenizer()
tokenized2 = tknzr.tokenize(content2)

print(tokenized2)
'''

stop_words=set(stopwords.words("english"))
stop_words.add('u')
stop_words.add('like')
stop_words.add('ur')
filtered=[]
for w in tokenized:
    if w not in stop_words:
        if (w.isnumeric() == False):
            filtered.append(w)

fdist = FreqDist(filtered)
fd = pd.DataFrame(fdist.most_common(50), columns = ["Topic","Frequency"]).reindex()

fig = px.bar(fd, x="Topic", y="Frequency")
fig.update_traces(marker_line_width=1.5)
fig.show()

'''keyword = "coronavirus"
counter = 0
for status in tweepy.Cursor(api.search, q=keyword, lang="en", include_entities=True, tweet_mode='extended').items(100000):
	counter += 1
	db.tweets_RESTapi.insert(status._json)
	if (counter % 1000 == 0):
		print (counter)

print("Done")'''

'''searchQuery = 'coronavirus'  # this is what we're searching for
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets.txt' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang="en", include_entities=True, tweet_mode='extended')
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId, lang="en", include_entities=True, tweet_mode='extended')
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang="en", include_entities=True, tweet_mode='extended', max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1), since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
'''


'''
keyword = "coronavirus"
maxTweets = 10000000
tweetsPerQry = 100
fName = 'tweets.txt'

sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

print(keyword[0])

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=keyword, count=tweetsPerQry, lang="en", include_entities=True)
                else:
                    new_tweets = api.search(q=keyword, count=tweetsPerQry,
                                            since_id=sinceId, lang="en", include_entities=True)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=keyword, count=tweetsPerQry,
                                            max_id=str(max_id - 1), lang="en", include_entities=True)
                else:
                    new_tweets = api.search(q=keyword, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId, lang="en", include_entities=True)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
'''

#print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

    #if (doc["text"]):
    #    print("----------------------------------------------------------")
    #    print (doc['text'])
    #    print("----------------------------------------------------------")


#print(db.tweets.count({"lang":"en"}))
