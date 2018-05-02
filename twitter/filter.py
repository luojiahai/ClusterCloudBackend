import couchdb

couch = couchdb.Server('http://localhost:5432/')
db = couch['tweets']

for id in db:
    doc = db[id] # to get the document by id
    try:
        if (not doc['coordinates']):
            db.delete(doc)
        elif ((doc['coordinates']['coordinates'][0] >= 113.6594 and doc['coordinates']['coordinates'][0] <= 153.61194) and (doc['coordinates']['coordinates'][1] >= -43.00311 and doc['coordinates']['coordinates'][1] <= -12.46113)):
            None
        else:
            db.delete(doc)
    except KeyError as e:
        db.delete(doc)
        continue

