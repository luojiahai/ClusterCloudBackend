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
    # twitter api stuff
    consumer_key = 'JLffJb3c9glRUc5E5OxiNZ1ry'
    consumer_secret = 'l8BiZHvqTxJ6CP2PDYDnQz6jc8ioBo82Zw49HDhFMkYyW9WJIz'
    access_token = '761644243-fLyz8h63avBSVDANarQ3NiBNuShsGjWuPnTgP0yN'
    access_secret = 'TlHnjqYLNBjTWMpLJ0kyO0vJ0PdgJgL5BayRljrfuWlKn'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    # database
    couch = couchdb.Server('http://localhost:5432/')
    db = couch['tweets_']

    # tweets pool
    tweets = []

    # constructor
    def __init__(self, scheduler):
        self.connections = []   # list of {"ip": HOST_NAME, "port": PORT_NUMBER}
        self.scheduler = scheduler
        self.master_host = ''
        self.master_port = ''
        self.my_host = ''
        self.my_port = ''

    # add connection con to connetions list
    def add_connection(self, con):
        self.connections.append({'ip': con['ip'], 'port': con['port']})
    
    # get conncetions list
    def get_connections(self):
        return self.connections
    
    # check if given ip addr contains in connections list
    def has_connection(self, ip):
        for connection in self.connections:
            if (connection['ip'] == ip):
                return True
        return False

    # delete a connection
    def delete_connection(self, ip):
        for connection in self.connections:
            if (connection['ip'] == ip):
                self.connections.remove(connection)

    # change the master connection
    def change_master(self):
        # delete the disconnected master
        for connection in self.connections:
            if (connection['ip'] in self.master_host):
                self.connections.remove(connection)
                # delete its worker as well
                self.scheduler.delete_worker(connection['ip'])
                break
        
        # sort the list of connections
        self.connections = sorted(self.connections, key=lambda k: k['ip']) 
        
        # choose ans set a new master - the first con in the list
        con = self.connections[0]
        self.master_host = con['ip']
        self.master_port = con['port']

    # set all connection information
    def set_config(self, master_host, master_port, my_host, my_port):
        self.master_host = master_host
        self.master_port = master_port
        self.my_host = my_host
        self.my_port = my_port

    # twitter stream listener class
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

    # twitter stream listen
    def listen(self):
        twitter_melbourne_stream = Stream(self.auth, self.MyListener())
        twitter_melbourne_stream.filter(locations=[113.6594,-43.00311,153.61194,-12.46113])

    # request for scheduling
    def request_schedule(self):
        while True:
            time.sleep(30)  # 30 seconds

            if (self.my_host in self.master_host):
                # broadcast to all other connections
                cons = {'connections': self.connections}
                for con in self.connections:
                    # if con is not myself
                    if (con['ip'] not in self.my_host):
                        try:
                            requests.post("http://" + con['ip'] + ":" + con['port'] + "/api/broadcast", json=cons)
                        except Exception as e:
                            # the connection is disconnected
                            print(e)
                            self.connections.remove(con)
                            self.scheduler.delete_worker(con['ip'])

            data = {'tasks': self.tweets}
            try:
                # request to schedule
                r = requests.post("http://" + self.master_host + ":" + self.master_port + "/api/schedule", json=data)
                self.tweets.clear()
            except Exception as e:
                print("REQUEST_SCHEDULE EXCEPTION CATCHED: " + str(e))
                # if no response, then change master
                self.change_master()
            