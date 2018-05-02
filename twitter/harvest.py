import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import couchdb

couch = couchdb.Server()
db = couch['tweets_']

consumer_key = 'JLffJb3c9glRUc5E5OxiNZ1ry'
consumer_secret = 'l8BiZHvqTxJ6CP2PDYDnQz6jc8ioBo82Zw49HDhFMkYyW9WJIz'
access_token = '761644243-fLyz8h63avBSVDANarQ3NiBNuShsGjWuPnTgP0yN'
access_secret = 'TlHnjqYLNBjTWMpLJ0kyO0vJ0PdgJgL5BayRljrfuWlKn'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            obj = json.loads(data)
            if (obj['coordinates']):
                try:
                    db[obj['id_str']] = obj
                except Exception as e:
                    None
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

twitter_melbourne_stream = Stream(auth, MyListener())
twitter_melbourne_stream.filter(locations=[113.6594,-43.00311,153.61194,-12.46113])
