# Import regular expressions to look for topics and mentions, json to parse tweet data
import re, json, operator
from collections import defaultdict as dd
import textblob
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

def one_button_start(text):
    print("bang~bang~bang~all start with a big bang~~~bang~")
    b = TextBlob(text)
    language = b.detect_language()
    spell_correctness = True
    if text != b.correct():
        spell_correctness = False
    text = str(b.correct())
    b1 = TextBlob(text)
    p = b1.sentiment.polarity
    s = b1.sentiment.subjectivity
    words = b1.words
    sentences = b1.sentences
    noun_phrases = b1.np_counts
    analysis_box =(language, spell_correctness, p,s,words,sentences, noun_phrases)
    return analysis_box
    
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
    testimonial = TextBlob(text)
    text2 = str(testimonial.correct())
    testimonial2 = TextBlob(text2)
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


def spell_check(text):
    correct = True
    b = TextBlob(text)
    if text != b.correct():
        correct = False
    return correct

def tokenize(text):
    '''take a tweet and return tokenized word list and list of sentences'''
    zen = TextBlob(text)
    words = zen.words
    sentences = zen.sentences
    return (words, sentences)

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

def get_sentiment_data(data_set):
    '''gather information about sentiment of tweets and return a dictionary
       of the stats'''
    data = []
    for doc in data_set:
        data.append(sentiment_analyze(doc))
    avg_polarity = 0
    avg_subjectivity = 0
    num_docs = len(data_set)

    stats = {'avg_polarity':avg_polarity,
             'avg_subjectivity':avg_subjectivity,
             'num_docs': num_docs}
    return stats

def extract_phrase(text):
    '''take a preprocessed tweet and return a dict of noun
       phrases and counts as value'''
    extractor = ConllExtractor()
    blob = TextBlob(text)
    return dict(blob.np_counts)


#test goes here
#print(extract_phrase('this is a test and good evening!'))
