from flask import Flask, session, redirect, url_for, escape, request
from schedule import *
from work import *
import json
import requests

app = Flask(__name__)

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
    

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
