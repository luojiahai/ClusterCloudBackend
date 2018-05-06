import couchdb
import requests
import json

couch = couchdb.Server('http://115.146.95.53:5432/')
db = couch['tweets']

skip = 1000000
limit = 100

while True:
    try:
        print("next loop: " + str(skip))
        uri = "http://readonly:ween7ighai9gahR6@45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary?include_docs=true&reduce=false&skip={}&limit={}".format(str(skip), str(limit))
        print(uri)
        response = requests.get(uri)

        data = response.json()
        rows = data['rows']

        for row in rows:
            try:
                doc = row['doc']
                del doc['_rev']
                id_str = doc['_id']
                db[id_str] = doc
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)
        continue
    
    skip += limit
