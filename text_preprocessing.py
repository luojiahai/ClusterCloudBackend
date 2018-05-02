#Import mpi so we can run on more than one node and processor
from mpi4py import MPI
# Import csv to read files and arguments
import csv, sys, getopt
# Import regular expressions to look for topics and mentions, json to parse tweet data
import re, json, operator, couchdb
from collections import defaultdict as dd

# Constants
MASTER_RANK = 0



def preprocess(text):
    hashtags = []
    hashtag = re.findall("(?:^|\s)#[a-z]{8,}(?=$|\s)",text)
    
    text = re.sub("(?:^|\s)#[a-z]{8,}(?=$|\s)","",text).strip()
    if hashtag:
        for h in hashtag:
            hashtags.append(h)
    return (hashtags, text)

''' preprocess the text and store in sadb, and return a dict of hashtags with frequency'''
def do_work(rank, db, size, sadb):
    i = 0
    hashtags = dd(int)
    tags = []
    for data_id in db:
        if i%size == rank:
            try:
                hashtags = dd(int)
                doc = db[data_id]
                text = doc['text']
                coor = doc['coordinates']
                tags, text = preprocess(text)
                processed_data = ({'text': text, 'coordinates':coor})
                sadb[str(doc['id'])] = processed_data
                for tag in tags:
                    hashtags[tag] += 1
            except:
                continue
            
        i += 1
            
    return hashtags

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


'''the result may be changed to required type before printing to terminal'''
def master_work_processor(comm, db, sadb):
    # Read our tweets
    rank = comm.Get_rank()
    size = comm.Get_size()

    results = do_work(rank, db, size, sadb)
    if size > 1:
        counts = marshall_work(comm)
        # Marshall that data
        for c in counts:
            for i in range(16):
                results[i] += c[i]
    #print result
    print(results)
    
    return None


def slave_work_processor(comm, db,sadb):
    # We want to process all relevant tweets and send our counts back
    # to master
    rank = comm.Get_rank()
    size = comm.Get_size()

    counts = do_work(rank, db, size, sadb)
    comm.send(counts, dest=MASTER_RANK, tag=MASTER_RANK)
        
def main():
    # Work out our rank, and run either master or slave process
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    couch = couchdb.Server('http://115.146.84.252:5432/')
    db = couch['tweets']
    sadb = couch['sentiment-analysis-tweets']
    if rank == 0 :
        # We are master
        master_work_processor(comm, db, sadb)
        print('in master')
    else:
        # We are slave
        slave_work_processor(comm, db, sadb)
        print('in slave')

# Run the actual program
if __name__ == "__main__":
    main()
                      

