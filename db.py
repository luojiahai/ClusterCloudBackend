import couchdb
import json

couch = couchdb.Server('http://115.146.84.252:5432/')
db = couch['tweets']

# get all the docs in db 'tweets'
for id in db:
    doc = db[id] # to get the document by id
    text = doc['text'] # to get the text field in one tweet document
    print(text)
    break
