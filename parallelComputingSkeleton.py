'''----------------------Usage of Parallel Computing Skeleton-------------


    Structure: main
                | master                     (slaves)
                    | master_processer        | slave_processer
                        | do_work  marshall      | do_work

 -------------------------------------------------------------------------                       
    To use this skeleton, you need to do the following steps:
    1. implement do_work and helper functions and return correct type
    2. change the input_file argument to database address
    3. change reading file to making quries
    4. Good luck
'''






# Import mpi so we can run on more than one node and processor
from mpi4py import MPI
# Import csv to read files and arguments
import csv, sys, getopt
# Import regular expressions to look for topics and mentions, json to parse tweet data
import re, json, operator, couchdb

# Constants
MASTER_RANK = 0


''' Fill in this function with the operation you want to do
    and return partial output'''
def do_work(rank, db, size):
    return None

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
def master_work_processor(comm, db):
    # Read our tweets
    rank = comm.Get_rank()
    size = comm.Get_size()

    results = do_work(rank, db, size)
    if size > 1:
        counts = marshall_work(comm)
        # Marshall that data
        for c in counts:
            for i in range(16):
                results[i] += c[i]
    #print result
    print(results)
    
    return None


def slave_work_processor(comm, db):
    # We want to process all relevant tweets and send our counts back
    # to master
    rank = comm.Get_rank()
    size = comm.Get_size()

    counts = do_work(rank, db, size)
    comm.send(counts, dest=MASTER_RANK, tag=MASTER_RANK)
        
def main():
    # Work out our rank, and run either master or slave process
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    db = couchdb.Server('http://115.146.84.252:5432/')['tweets']
    if rank == 0 :
        # We are master
        master_work_processor(comm, db)
        print('in master')
    else:
        # We are slave
        slave_work_processor(comm, db)
        print('in slave')

# Run the actual program
if __name__ == "__main__":
    main()
                      
