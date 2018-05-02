import couchdb
import json

couch = couchdb.Server('http://115.146.84.252:5432/')
# couch = couchdb.Server()
db = couch['tweets']
sadb = couch['sentiment-analysis-tweets']

# get all the docs in db 'tweets'
for id in db:
    try:
        doc = db[id] # to get the document by id
        text = doc['text'] # to get the text field in one tweet document
        coordinates = doc['coordinates']
        print(text)
        ## do analysis here
        sentiment_score = 0.5
        ## then save to sadb
        sadb[str(doc['id'])] = {'text': text, 'sentiment': sentiment_score, 'coordinates': coordinates}
    except KeyError as e:
        # handle no such key 'text' or 'coordinates'
        None
    # break


# map_fun = '''
# function(doc) {
#     emit(doc._id, {text: doc.text, sentiment: doc.sentiment});
# }
# '''

# results = sadb.query(map_fun)

# print(results.rows)