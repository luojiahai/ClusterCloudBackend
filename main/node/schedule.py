class Scheduler:
    def __init__(self):
        self.workers = []
        self.pool = []

    def get_workers(self):
        return self.workers

    def add_worker(self, worker):
        self.workers.append({'ip': worker['ip'], 'port': worker['port'], 'working': False})

    def delete_worker(self, ip):
        for worker in self.workers:
            if (worker['ip'] == ip):
                self.workers.remove(worker)
                break

    def has_worker(self, ip):
        for worker in self.workers:
            if (worker['ip'] == ip):
                return True
        return False

    def run_schedule(self, tasks):
        # do something with the tasks, please multi-threaded and organise pool
        string = "["
        for task in tasks:
            string += task + ", "
        string += "]"
        print("SCHEDULE RUN: " + string)
        None
