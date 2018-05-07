# ClusterCloudBackend

## Libraries

Install Flask

```
pip install flask
```

Run API

```
python restful.py -a {MY_HOST_NAME} -b {MY_PORT_NUMBER} -c {MASTER_HOST_NAME} -d {MASTER_PORT_NUMBER}
```

db docs

http://couchdb-python.readthedocs.io


Install sentiment analysis dependencies
```
pip install textBlob
pip install numpy
pip install scikit-learn
pip install nltk
```
## Use Parallel Computing Framework

To use parallel programming in your work, modify
```
parallelComputingSkeleton.py
```
in your branch.

Find the function ```do_work(rank, input_file, size)``` and it looks like this:
```
def do_work(rank, input_file, size):
    return None
```
Change it to your desired function and make sure it returns the output.

Find the function ```marshall_work(comm)``` , where it looks like:
```
def marshall_work(comm):
    processes = comm.Get_size()
    #TODO: change it to your desired result type
    results = []
    
    for i in range(processes-1):
    # Receive data
        results.append(comm.recv(source=(i+1), tag=MASTER_RANK))

    #TODO: manipulate with the list of results received from all processors
    #      and print out the result
    return results
  ```
  Modify it to suit your needs.
  
  Finally, change the ```input_file``` argument to a database query,
  which I have no idea of how to do.
