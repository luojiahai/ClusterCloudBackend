import requests
import threading

class Scheduler:
    # constructor
    def __init__(self):
        self.workers = {}   # "HOST_NAME": {"ip": HOST_NAME, "port": PORT_NUMBER, "working": IS_WORKING}
        self.pool = {}      # pool
        self.threads = []   # threads list

    # get workers list
    def get_workers(self):
        return self.workers

    # add worker to workers list
    def add_worker(self, worker):
        self.workers[worker['ip']] = {'ip': worker['ip'], 'port': worker['port'], 'working': False}
        self.pool[worker['ip']] = []

    # delete a worker by given ip addr
    def delete_worker(self, ip):
        try:
            del self.workers[ip]
            del self.pool[ip]
        except KeyError as e:
            print("DELETE_WORKER: KEYERROR")
    
    # check if given ip addr contains in workers list
    def has_worker(self, ip):
        return ip in self.workers

    # organize the pool
    def organize_pool(self, tasks):
        for task in tasks:
            sorted_keys = sorted(self.pool, key=lambda k: len(self.pool[k]))
            self.pool[sorted_keys[0]].append(task)  # the least tasks worker

    # request to a worker for doing work
    def do_work(self, worker, tasks):
        self.workers[worker['ip']]['working'] = True
        data = {'tasks': tasks}
        requests.post('http://' + worker['ip'] + ':' + worker['port'] + '/api/work', json=data)
        self.workers[worker['ip']]['working'] = False

    # scheduling
    def run_schedule(self, tasks):
        print("---------DEBUG----------RUN_SCHEDULE")
        print("SCHEDULING TASK: ")
        for task in tasks:
            print(task)
        print("---------DEBUG---------/RUN_SCHEDULE")

        # organize pool
        self.organize_pool(tasks)

        # request to work
        for worker_k, worker_v in self.workers.items():
            # if the worker running a job, then skip
            if (worker_v['working']):
                continue
            else:
                tasks = list(self.pool[worker_k])   # copy instead of reference
                self.pool[worker_k] = []            # clear after copy
                # start a thread
                t = threading.Thread(target=self.do_work, args=(worker_v, tasks))
                self.threads.append(t)
                t.start()
