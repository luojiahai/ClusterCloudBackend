import couchdb
import json

couch = couchdb.Server()
db = couch['tweets']

with open('tweets.json') as f:
    for line in f:
        obj = json.loads(line)
        db.save(obj)