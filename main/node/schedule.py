import requests

class Scheduler:
    def __init__(self):
        self.workers = []   # worker {"ip": HOST_NAME, "port": PORT_NUMBER, "working": IS_WORKING}
        self.pool = []      # pool

    def get_workers(self):
        return self.workers

    def add_worker(self, worker):
        self.workers.append({'ip': worker['ip'], 'port': worker['port'], 'working': False})
        # worker {"ip": HOST_NAME, "port": PORT_NUMBER, "working": IS_WORKING}
        
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

    def do_work(self, worker, tasks):
        data = {'tasks': tasks}
        requests.post('http://' + worker['ip'] + ':' + worker['port'] + '/api/work', json=data)

    def run_schedule(self, tasks):
        # do something with the tasks, please multi-threaded and organise pool
        ### ### ###

        # print tasks for testing
        for task in tasks:
            print(task)
            
        # request to work
        ### ### ### this is a simple one, should divide tasks to workers and do multi-thread
        for worker in self.workers:
            self.do_work(worker, tasks)
