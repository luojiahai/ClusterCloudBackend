import couchdb

couch = couchdb.Server()
new_db = couch['tweets_']
old_db = couch['tweets']

for id in old_db:
    doc = old_db[id]
    id_str = doc['id_str']
    try:
        new_db[id_str] = doc
        print(id_str)
    except Exception as e:
        print("WTF")
    break
