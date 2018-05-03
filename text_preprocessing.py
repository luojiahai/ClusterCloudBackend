# Import regular expressions to look for topics and mentions, json to parse tweet data
import re, json, operator
from collections import defaultdict as dd
import textBlob

    
def extract_hashtags(text):
    '''take a raw tweet and return a list of hashtags'''
    hashtags = []
    hashtag = re.findall("(?:^|\s)#[a-z]{8,}(?=$|\s)",text)
    if hashtag:
        for h in hashtag:
            hashtags.append(h)
    return hashtags

def sentiment_analyze(text):
    '''take a tweet without hashtags and return sentiment values'''
    testimonial1 = TextBlob(text)
    text = testimonial.correct()
    testimonial2 = TextBlob(text)
    polarity = testimonial2.sentiment.polarity
    subjectivity = testimonial2.sentiment.subjectivity
    return (polarity, subjectivity)

def create_hashtag_dict(data_set):
    '''take a list of tweets, extract hashtags, and create a dictionary
       of hashtags where the values are tweet_id in couchdb'''
    hashtag_dict = dd(list)
    for doc in data_set:
        text = doc['text']
        doc_id = doc['id']
        tags = extract_hashtags(text)
        for tag in tags:
            hashtag_dict[tag].append(doc_id)
    return hashtag_dict

def get_tweets_in_range(ux,uy,bx,by, data_set):
    '''get tweets in a certain geographical range'''
    data = []
    for doc in data_set:
        try:
            coor = doc['coordinates']
            if bx<=coor[0]<=ux and by<=coor[1]<=uy:
                tweet = {'id':doc['id'],'text':doc['text']}
                data.append(tweet)
        except:
            continue
    return data
            
        
