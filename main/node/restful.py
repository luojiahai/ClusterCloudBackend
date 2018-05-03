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
            # do something here, to store connection
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
        workers = request.json['workers']
        for worker in workers:
            if (not scheduler.has_worker(worker['ip'])):
                scheduler.add_worker(worker)
            else:
                print("ROUTE /api/broadcast POST: WORKER EXIST " + worker['ip'] + ":" + worker['port'])
        return "ROUTE /api/broadcast POST: BROADCAST DONE"
    return '''
        ROUTE /api/broadcast GET: 
        {
            "workers" : [{WORKER}]
        }
    '''

@app.route('/change_master')
def change_master():
    # do something here to change a different master master
    None

def make_connection(argv):
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
    
    # myself is a worker
    worker = {'ip': host, 'port': port}
    scheduler.add_worker(worker)

    # if me not the master
    if (host not in master):
        # do connect to master
        r = requests.post(master + "/api/connect", data = {'ip': host, 'port':port})
        print(r)
        None

if __name__ == '__main__':
    make_connection(sys.argv[1:])

    t1 = threading.Thread(target=fetcher.listen)
    t1.start()

    t2 = threading.Thread(target=fetcher.request_work)
    t2.start()

    app.run(threaded=True, debug=False)
