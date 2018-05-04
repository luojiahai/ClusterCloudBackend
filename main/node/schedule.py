import requests

class Scheduler:
    # constructor
    def __init__(self):
        self.workers = {}   # "HOST_NAME": {"ip": HOST_NAME, "port": PORT_NUMBER, "working": IS_WORKING}
        self.pool = []      # pool

    # get workers list
    def get_workers(self):
        return self.workers

    # add worker to workers list
    def add_worker(self, worker):
        self.workers[worker['ip']] = {'ip': worker['ip'], 'port': worker['port'], 'working': False}
    
    # delete a worker by given ip addr
    def delete_worker(self, ip):
        try:
            del self.workers[ip]
        except KeyError as e:
            print("DELETE_WORKER: KEYERROR")
    
    # check if given ip addr contains in workers list
    def has_worker(self, ip):
        return ip in self.workers

    # request to a worker for doing work
    def do_work(self, worker, tasks):
        data = {'tasks': tasks}
        requests.post('http://' + worker['ip'] + ':' + worker['port'] + '/api/work', json=data)

    # scheduling
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
