from flask import Flask, session, redirect, url_for, escape, request
from schedule import *
from work import *
from fetch import *
import json
import requests

app = Flask(__name__)

scheduler = Scheduler()
worker = Worker()
fetcher = Fetcher("http://127.0.0.1:5000/")

@app.route('/')
def index():
    return 'HELLO, WORLD!'

@app.route('/api/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        data = request.json
        if (scheduler.has_worker(data['ip'])):
            return "WORKER EXISTED"
        else:
            scheduler.add_worker(data)
            # do something here, to store connection
            return "CONNECT SUCCESS"
    return json.dumps(scheduler.get_workers())

@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        data = request.json['tasks']
        scheduler.run(data)
        return "SCHEDULE DONE"
    return '''
        {
            "tasks" : [{TWEET_ID}]
        }
    '''

@app.route('/api/work', methods=['GET', 'POST'])
def work():
    if request.method == 'POST':
        data = request.json['tasks']
        worker.run(data)
        return "WORK DONE"
    return '''
        {
            "tasks" : [{TWEET_ID}]
        }
    '''

@app.route('/change_master')
def change_master():
    # do something here to change a different master master
    None


def run_api():
    app.run(threaded=True, debug=True)

if __name__ == '__main__':
    threads = []

    t1 = threading.Thread(target=fetcher.listen)
    threads.append(t1)
    t1.start()

    t2 = threading.Thread(target=fetcher.work)
    threads.append(t2)
    t2.start()

    t3 = threading.Thread(target=run_api)
    threads.append(t3)
    t3.start
    
