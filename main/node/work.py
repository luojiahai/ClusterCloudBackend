import couchdb

class Worker:
    couch = couchdb.Server()
    tweets_db = couch['tweets_']
    sa_tweets_db = couch['sentiment-analysis-tweets_']

    def __init__(self):
        None
    
    def analyse(self, text):
        # do sentiment analysis here
        ### ### ###
        return 0.5

    def run_work(self, tasks):
        for task in tasks:
            try:
                # get neccessary data
                tweet = self.tweets_db[task]        # get the tweet by id
                text = tweet['text']                # get the text
                score = self.analyse(text)          # get the sentiment score here
                id_str = tweet['_id']               # get the id
                coordinates = tweet['coordinates']  # get the coordinates

                print("analysed: " + text)

                # save data to sa_tweets_db
                self.sa_tweets_db[id_str] = {
                                    'text': text, 
                                    'score': score, 
                                    'coordinates': coordinates
                                } # maybe more to save
            except KeyError as e:
                continue
