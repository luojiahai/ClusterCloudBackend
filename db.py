import couchdb
import json

couch = couchdb.Server()
db = couch['tweets']

# get all the docs in db 'tweets'
for id in db:
    doc = db[id]
    print(doc)
