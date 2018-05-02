workers = {}

def addWorker(worker):
    workers[worker['ip']] = {'port': worker['port'], 'working': False}

def deleteWorker(ip):
    del workers[ip]

def hasWorker(ip):
    return ip in workers

def schedule():
    None

