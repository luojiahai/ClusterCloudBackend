class Scheduler:
    def __init__(self, master_ip, master_port):
        self.master = master_ip + ':' + master_port
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

    # def add_task(self, task):
    #     self.pool.append(task)

    def change_master(self, master_ip, master_port):
        self.master = master_ip + ':' + master_port

    def run(self, tasks):
        # do something with the tasks
        None

scheduler = Scheduler('http://127.0.0.1', '5000')
