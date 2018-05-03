import sys
import getopt
from flask import Flask, session, redirect, url_for, escape, request
from schedule import *
from work import *
from fetch import *
import json
import requests

app = Flask(__name__)

master = "http://127.0.0.1:5000"

scheduler = Scheduler()
worker = Worker()
fetcher = Fetcher(master)

@app.route('/')
def index():
    return 'HELLO, WORLD!'

@app.route('/api/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        data = request.json
        if (scheduler.has_worker(data['ip'])):
            return "ROUTE /api/connect POST: WORKER EXISTED"
        else:
            scheduler.add_worker(data)
            return "ROUTE /api/connect POST: CONNECT SUCCESS"
    return json.dumps(scheduler.get_workers())

@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        data = request.json['tasks']
        scheduler.run_schedule(data)
        return "ROUTE /api/schedule POST: SCHEDULE DONE"
    return '''
        ROUTE /api/schedule GET: 
        {
            "tasks" : [{TWEET_ID}]
        }
    '''

@app.route('/api/work', methods=['GET', 'POST'])
def work():
    if request.method == 'POST':
        data = request.json['tasks']
        worker.run_work(data)
        return "ROUTE /api/work POST: WORK DONE"
    return '''
        ROUTE /api/work GET: 
        {
            "tasks" : [{TWEET_ID}]
        }
    '''

@app.route('/api/broadcast', methods=['GET', 'POST'])
def broadcast():
    if request.method == 'POST':
        connections = request.json['connections']
        for con in connections:
            if (not scheduler.has_worker(con['ip'])):
                scheduler.add_worker(con)
            if (not fetcher.has_connection(con['ip'])):
                fetcher.add_connection(con)
            else:
                print("ROUTE /api/broadcast POST: CON EXIST " + con['ip'] + ":" + con['port'])
        return "ROUTE /api/broadcast POST: BROADCAST DONE"
    return '''
        ROUTE /api/broadcast GET: 
        {
            "connections" : [{WORKER}]
        }
    '''

def initialize(argv):
    host = ''
    port = ''
    try:
        opts, args = getopt.getopt(argv, "h:p:", ["host=","port="])
    except getopt.GetoptError:
        print('usage: restful.py -h {HOST_NAME} -p {PORT_NUMBER}')
        sys.exit(2)
    if (len(opts) != 2):
        print('usage: restful.py -h {HOST_NAME} -p {PORT_NUMBER}')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = arg
    
    # add myself to workers and connections
    worker = {'ip': host, 'port': port}
    scheduler.add_worker(worker)
    fetcher.add_connection(worker)

    # broadcast
    for con in fetcher.get_connections():
        if (host not in con['ip']):
            # if not myself
            requests.post(master + "/api/broadcast", data = {'ip': con['ip'], 'port': con['port']})

    # if myself is master, then do fetch
    if (host in master):
        t1 = threading.Thread(target=fetcher.listen)
        t1.start()

        t2 = threading.Thread(target=fetcher.request_work)
        t2.start()

if __name__ == '__main__':
    initialize(sys.argv[1:])
    app.run(threaded=True, debug=False)
