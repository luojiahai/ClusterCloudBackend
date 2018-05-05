import couchdb
from text_preprocessing import *

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
        '''get a text and return a tuple of stats,
           0. language: a string representing language
           1. spell_correctness: boolean
           2. polarity: float from -1 to 1
           3. subjectivity: float from 0 to 1
           4. words: a list of lemmatized words
           5. sentences: a list of sentences
           6. a dictionary of noun phrase counts'''
        analysis_box = one_button_start(text)
        return analysis_box

    # working
    def run_work(self, tasks):
        print("---------DEBUG----------RUN_WORK")
        print("RUNNING WORK: ")
        for task in tasks:
            try:
                # get neccessary data
                tweet = self.tweets_db[task]        # get the tweet by id
                text = tweet['text']                # get the text
                box = self.analyse(text)          # get the sentiment score here
                id_str = tweet['_id']               # get the id
                coordinates = tweet['coordinates']  # get the coordinates

                print("========================")
                print("ANALYSING: " + text)
                
                noun_phrases_dict = {}
                for k, v in box[6].items():
                    noun_phrases_dict[str(k)] = v
                
                sentences = []
                for sentence in box[5]:
                    sentences.append(str(sentence))
                
                # save data to sa_tweets_db
                self.sa_tweets_db[id_str] = {
                                    'text': text,
                                    'coordinates': coordinates,
                                    'language': box[0],
                                    'spell_correctness': box[1],
                                    'polarity': box[2],
                                    'subjectivity': box[3],
                                    'words': box[4],
                                    'sentences': sentences,
                                    'noun_phrases': noun_phrases_dict
                                } # maybe more to save
            except KeyError as e:
                continue
        print("---------DEBUG---------/RUN_WORK")
