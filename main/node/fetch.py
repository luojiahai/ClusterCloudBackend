import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import couchdb
import time
import threading
import requests

class Fetcher:
    consumer_key = 'JLffJb3c9glRUc5E5OxiNZ1ry'
    consumer_secret = 'l8BiZHvqTxJ6CP2PDYDnQz6jc8ioBo82Zw49HDhFMkYyW9WJIz'
    access_token = '761644243-fLyz8h63avBSVDANarQ3NiBNuShsGjWuPnTgP0yN'
    access_secret = 'TlHnjqYLNBjTWMpLJ0kyO0vJ0PdgJgL5BayRljrfuWlKn'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    couch = couchdb.Server()
    db = couch['tweets_']

    tweets = []

    def __init__(self, default_master):
        self.master = default_master
        self.connections = []
    
    def add_connection(self, con):
        self.connections.append(con)
        # {"ip": HOST_NAME, "port": PORT_NUMBER}

    def change_master(self):
        # choose a new master
        con = {'ip': 'hostname', 'port': 'port'}
        self.master = 'http://' + con['ip'] + ':' + con['port']

    class MyListener(StreamListener):
        def on_data(self, data):
            try:
                obj = json.loads(data)
                if (obj['coordinates']):
                    try:
                        id_str = obj['id_str']
                        Fetcher.db[id_str] = obj
                        Fetcher.tweets.append(id_str)
                    except Exception as e:
                        print("EXCEPTION: LISTENER")
                return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
            return True
            
        def on_error(self, status):
            print("ON_ERROR: " + str(status))
            return True

    def listen(self):
        twitter_melbourne_stream = Stream(self.auth, self.MyListener())
        twitter_melbourne_stream.filter(locations=[113.6594,-43.00311,153.61194,-12.46113])

    def request_work(self):
        while True:
            time.sleep(30)

            data = {'tasks': self.tweets}
            try:
                # request schedule
                r = requests.post(self.master + "/api/schedule", json=data)
                print(r)
                self.tweets.clear()
            except Exception as e:
                # if no response, then no connection
                self.change_master()
                None
            
