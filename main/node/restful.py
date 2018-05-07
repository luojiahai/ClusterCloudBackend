import sys
import getopt
from flask import Flask, session, redirect, url_for, escape, request
from schedule import *
from work import *
from fetch import *
import json
import requests

app = Flask(__name__)

# default master
master_host = ''
master_port = ''

# my hostname and portnumber
my_host = ''
my_port = ''

# instances of functional module
scheduler = Scheduler()
worker = Worker()
fetcher = Fetcher(scheduler)

# ============================= restful routing ============================= #

@app.route('/')
def index():
    return 'HELLO, WORLD!'

@app.route('/api/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        data = request.json
        if (fetcher.has_connection(data['ip'])):
            return "ROUTE /api/connect POST: CONNECTION EXISTED"
        else:
            # add to connections and workers list
            fetcher.add_connection(data)
            scheduler.add_worker(data)
            return "ROUTE /api/connect POST: CONNECT SUCCESS"
    return json.dumps(fetcher.get_connections())

@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        data = request.json['tasks']
        scheduler.run_schedule(data)
        return "ROUTE /api/schedule POST: SCHEDULE DONE"
    return '''
        ROUTE /api/schedule GET: 
        {
            "tasks" : [TWEET_ID]
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
            "tasks" : [TWEET_ID]
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
        for i in fetcher.get_connections():
            flag = False
            for j in connections:
                if (i['ip'] == j['ip']):
                    flag = True
                    break
            if not flag:
                fetcher.delete_connection(i['ip'])
                scheduler.delete_worker(i['ip'])
        return "ROUTE /api/broadcast POST: BROADCAST DONE"
    return '''
        ROUTE /api/broadcast GET: 
        {
            "connections" : [{CONNECTION where "ip": HOSTNAME, "port": PORTNUMBER}]
        }
    '''

# =========================================================================== #

# initialize a conneciton
def initialize(argv):
    # command line arguments
    try:
        opts, args = getopt.getopt(argv, "a:b:c:d:", ["masterhost=","masterport","host=","port="])
    except getopt.GetoptError:
        print('usage: restful.py -a {MASTER_HOST_NAME} -b {MASTER_PORT_NUMBER} -c {MY_HOST_NAME} -d {MY_PORT_NUMBER}')
        sys.exit(2)
    if (len(opts) != 4):
        print('usage: restful.py -a {MASTER_HOST_NAME} -b {MASTER_PORT_NUMBER} -c {MY_HOST_NAME} -d {MY_PORT_NUMBER}')
        sys.exit(2)
    for opt, arg in opts:
        global master_host
        global master_port
        global my_host
        global my_port
        if opt in ("-a", "--host"):
            my_host += str(arg)
        elif opt in ("-b", "--port"):
            my_port += str(arg)
        elif opt in ("-c", "--masterhost"):
            master_host += str(arg)
        elif opt in ("-d", "--masterport"):
            master_port += str(arg)
    
    fetcher.set_config(master_host, master_port, my_host, my_port)

    # add myself to workers and connections
    worker = {'ip': my_host, 'port': my_port}
    scheduler.add_worker(worker)
    fetcher.add_connection(worker)

    # connect to master if me not master
    if (my_host not in master_host):
        uri_str = "http://admin:admin@{}:5986/_nodes/couchdb@{}".format(master_host, my_host)
        requests.put(uri_str, data={})
        requests.post("http://" + master_host + ":" + master_port + "/api/connect", json={'ip': my_host, 'port': my_port})

    # if myself is master
    if (my_host in master_host):
        # start listenr thread for harvesting tweets
        t1 = threading.Thread(target=fetcher.listen)
        t1.start()
        # start request_schedule thread for requesting schedule every 30s
        t2 = threading.Thread(target=fetcher.request_schedule)
        t2.start()
    # if myself is not master
    else:
        t1 = threading.Thread(target=fetcher.request_schedule)
        t1.start()

# main
if __name__ == '__main__':
    initialize(sys.argv[1:])
    app.run(threaded=True, debug=False, host=my_host, port=int(my_port))
