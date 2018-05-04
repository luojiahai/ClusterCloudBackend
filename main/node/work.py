import couchdb

class Worker:
    # database
    couch = couchdb.Server()
    tweets_db = couch['tweets_']
    sa_tweets_db = couch['sentiment-analysis-tweets_']

    # constructor
    def __init__(self):
        None
    
    # analysis function
    def analyse(self, text):
        ### ### ### sentiment analysis
        return 0.5

    # working
    def run_work(self, tasks):
        print("---------DEBUG----------RUN_WORK")
        print("RUNNING WORK: ")
        for task in tasks:
            try:
                # get neccessary data
                tweet = self.tweets_db[task]        # get the tweet by id
                text = tweet['text']                # get the text
                score = self.analyse(text)          # get the sentiment score here
                id_str = tweet['_id']               # get the id
                coordinates = tweet['coordinates']  # get the coordinates

                print("========================")
                print("ANALYSING: " + text)
                
                # save data to sa_tweets_db
                self.sa_tweets_db[id_str] = {
                                    'text': text, 
                                    'score': score, 
                                    'coordinates': coordinates
                                } # maybe more to save
            except KeyError as e:
                continue
        print("---------DEBUG---------/RUN_WORK")
