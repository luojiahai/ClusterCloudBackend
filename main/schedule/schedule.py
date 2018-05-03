class Scheduler:
    def __init__(self):
        self.workers = {}
        self.pool = []

    def getWorkers(self):
        return self.workers

    def addWorker(self, worker):
        self.workers[worker['ip']] = {'port': worker['port'], 'working': False}

    def deleteWorker(self, ip):
        del self.workers[ip]

    def hasWorker(self, ip):
        return ip in self.workers

    def addTask(self, task):
        self.pool.append(task)

    def run(self, tasks):
        # do something with the tasks
        None

scheduler = Scheduler()
