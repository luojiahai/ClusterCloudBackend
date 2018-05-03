class Scheduler:
    def __init__(self):
        self.workers = {}
        self.pool = {}

    def get_workers(self):
        return self.workers

    def add_worker(self, worker):
        self.workers[worker['ip']] = {'port': worker['port'], 'working': False}

    def delete_worker(self, ip):
        del self.workers[ip]

    def has_worker(self, ip):
        return ip in self.workers

    def run(self, tasks):
        # do something with the tasks, please multi-threaded and organise pool
        None
