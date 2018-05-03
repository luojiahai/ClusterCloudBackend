import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import couchdb
import time
import threading
import requests
from flask import Flask, session, redirect, url_for, escape, request
import json

app = Flask(__name__)

default_master = 'http://127.0.0.1' + ':' + '3000'
connections = []

couch = couchdb.Server()
db = couch['tweets_']

consumer_key = 'JLffJb3c9glRUc5E5OxiNZ1ry'
consumer_secret = 'l8BiZHvqTxJ6CP2PDYDnQz6jc8ioBo82Zw49HDhFMkYyW9WJIz'
access_token = '761644243-fLyz8h63avBSVDANarQ3NiBNuShsGjWuPnTgP0yN'
access_secret = 'TlHnjqYLNBjTWMpLJ0kyO0vJ0PdgJgL5BayRljrfuWlKn'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

tweets = []

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            obj = json.loads(data)
            if (obj['coordinates']):
                try:
                    id_str = obj['id_str']
                    db[id_str] = obj
                    tweets.append(id_str)
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

def listen():
    twitter_melbourne_stream.filter(locations=[113.6594,-43.00311,153.61194,-12.46113])

def work():
    while True:
        time.sleep(30)
        print(tweets)
        tweets.clear()

def test_connection():
    while True:
        time.sleep(60)
        try:
            content = requests.get(default_master + '/api/connect').content
            return True
        except Exception as e:
            # do something here
            print("DOWN!")
            return False

threads = []

t1 = threading.Thread(target=listen)
threads.append(t1)
t1.start()

t2 = threading.Thread(target=work)
threads.append(t2)
t2.start()

t3 = threading.Thread(target=test_connection)
threads.append(t3)
t3.start()