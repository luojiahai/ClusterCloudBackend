from flask import Flask, session, redirect, url_for, escape, request
from schedule import *
from work import *
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'HELLO, WORLD!'

@app.route('/api/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        data = request.json
        if (scheduler.hasWorker(data['ip'])):
            return "WORKER EXISTED"
        else:
            scheduler.addWorker(data)
            return "CONNECT SUCCESS"
    return json.dumps(scheduler.getWorkers())

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
        for e in data:
            worker.run(e)
        return "WORK DONE"
    return '''
        {
            "tasks" : [{TWEET_ID}]
        }
    '''

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
