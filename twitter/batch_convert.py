import couchdb
import requests
import json

couch = couchdb.Server('http://115.146.95.53:5432/')
db = couch['tweets']

skip = 0
limit = 100

while True:
    uri = "http://readonly:ween7ighai9gahR6@45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary?include_docs=true&reduce=false&skip={}&limit={}".format(str(skip), str(limit))
    response = requests.get(uri)

    data = response.json()
    rows = data['rows']

    for row in rows:
        try:
            doc = row['doc']
            db[doc['_id']] = doc
        except Exception as e:
            print(e)
            continue
    
    skip += limit
