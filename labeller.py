import couchdb
import json

couch = couchdb.Server('http://115.146.84.252:5432/')
db_tweets = couch['tweets']
db_labelled_tweets = couch['labelled-tweets']

# get all the docs in db 'tweets'
for id in db_tweets:
    doc = db_tweets[id] # to get the document by id
    if str(doc['id']) in db_labelled_tweets:
        continue
    else:
        text = doc['text'] # to get the text field in one tweet document
        print("text: \n" + text)
        label = -1
        while True:
            string = input("enter label: ")
            if str.isdigit(string) and (int(string) == 0 or int(string) == 1):
                label = int(string)
                break
            else:
                print("please enter 0 or 1")
        db_labelled_tweets[str(doc['id'])] = {'text': doc['text'], 'label': label}
