import couchdb

class Worker:
    def __init__(self):
        couch = couchdb.Server()
        self.tweets_db = couch['tweets_']
        self.sa_tweets_db = couch['sentiment-analysis-tweets_']
        None
    
    def analyse(self, text):
        # do sentiment analysis here
        return 0.5

    def run(self, task):
        try:
            tweet = self.tweets_db[task]        # get the tweet by id
            text = tweet['text']                # get the text
            score = self.analyse(text)          # get the sentiment score here
            id_str = tweet['_id']               # get the id
            coordinates = tweet['coordinates']  # get the coordinates

            print(text)

            # save to sa_tweets_db
            self.sa_tweets_db[id_str] = {
                                'text': text, 
                                'score': score, 
                                'coordinates': coordinates
                            } # maybe more to save
            
        except KeyError as e:
            print(e)
            None
        None
    
worker = Worker()
