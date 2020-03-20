from pymongo import MongoClient
import tweepy
import json
import credentials

#Authenticates to the Twitter API
class TwitterAuthenticator():
    def authenticate(self):
        auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)
        return auth

#The streaming class that initialises the authenticator and defines the parameters to stream
class TwitterStreamer():
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self):
        auth = self.twitter_autenticator.authenticate()
        streamer = tweepy.streaming.Stream(auth, MyStreamListener(tweepy.API(auth)))
        streamer.sample(languages=["en"])

#The stream listener that stores the tweet data into the db and handles errors
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.db = MongoClient().twitterdb

    def on_data(self, tweet):
        self.db.tweet_storage.insert(json.loads(tweet))

    def on_timeout(self):
        print >> sys.stderr, 'Timeout.....'
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print(420)
            return False
        else:
            print ('An Error has occurred: ' + repr(status_code))
            return True

#Starts the streaming process
if __name__ == '__main__':
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets()
