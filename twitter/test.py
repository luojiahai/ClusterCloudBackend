import couchdb
import requests
import json

couch = couchdb.Server('http://115.146.95.53:5432/')
db = couch['instagram']

with open('tinyInstagram.json') as f:
    next(f)
    for line in f:
        try:
            json_str = line[:len(line)-2]
            obj = json.loads(json_str)
            db[obj['id']] = obj
        except Exception as e:
            print(e)
            continue
        