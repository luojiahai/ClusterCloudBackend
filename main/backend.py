# This file was created by Geoffrey Ka-Hoi Law and modified by Zhe Tang.
import sys
import getopt
from flask import Flask, Response
import couchdb
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

couch = couchdb.Server('http://localhost:5432/')
db = couch['sentiment-analysis-tweets_']

@app.route("/")
def hello():
    return "Hello World!"

# Filter limit numbers of sentiment data from couchDB
# and rearrange them into GeoJson style.
@app.route("/get1")
def get1():
    rows = db.view("test-doc/new-view-01", descending='true', limit=2048)
    response = {
            "type": "FeatureCollection",
            "features": []
        }
    for row in rows:
        feature = {
                "type": "Feature",
                "geometry": row.value[0],
                "properties": {
                    "id": row.id,
                    "polarity": row.value[1],
                    "coordinates": row.value[0]["coordinates"]
                }
            }
        response["features"].append(feature)
    return Response(json.dumps(response), mimetype="application/json")

# Filter missspelling data from couchDB
# and rearrange them into GeoJson style.
@app.route("/get4")
def get4():
    rows = db.view("test-doc/new-view-04")
    response = {
            "type": "FeatureCollection",
            "features": []
        }
    for row in rows:
        feature = {
                "type": "Feature",
                "geometry": row.key,
                "properties": {
                    "id": row.id,
                    "coordinates": row.key["coordinates"]
                }
            }
        response["features"].append(feature)
    return Response(json.dumps(response), mimetype="application/json")

# Reduce view and get top 10 popular hashtags.
@app.route("/getHashTags")
def getHashTags():
    rows = db.view("test-doc/new-view-02", group='true')
    top10 = []
    for row in rows:
        if len(top10) < 10:
            top10.append((row.value,row.key))
            top10.sort()
        else:
            if row.value > top10[0][0]:
                top10[0] = (row.value,row.key)
                top10.sort()
    top10.sort(reverse=True)
    response = [{'hashtag': tag[1], 'count': tag[0]} for tag in top10]
    return Response(json.dumps(response), mimetype="application/json")

# Filter particular Hashtag data from couchDB
# and rearrange them into GeoJson style.
@app.route("/hashTag/<tagName>")
def hashTag(tagName):
    rows = db.view("test-doc/new-view-02", key=tagName, reduce='false')
    response = {"type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": row.value[0],
                "properties": {
                    "id": row.id,
                    "polarity": row.value[1],
                    "coordinates": row.value[0]["coordinates"]
                }
            }for row in rows]}
    return Response(json.dumps(response), mimetype="application/json")

# Reduce view and get top 10 popular language.
@app.route("/getLan")
def getLan():
    rows = db.view("test-doc/new-view-03", group='true')
    top10 = []
    for row in rows:
        if len(top10) < 10:
            top10.append((row.value,row.key))
            top10.sort()
        else:
            if row.value > top10[0][0]:
                top10[0] = (row.value,row.key)
                top10.sort()
    top10.sort(reverse=True)
    response = [{'language': tag[1], 'count': tag[0]} for tag in top10]
    return Response(json.dumps(response), mimetype="application/json")

# Filter particular language data from couchDB
# and rearrange them into GeoJson style.
@app.route("/language/<lanName>")
def language(lanName):
    rows = db.view("test-doc/new-view-03", key=lanName, reduce='false')
    response = {"type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": row.value,
                "properties": {
                    "id": row.id,
                    "coordinates": row.value["coordinates"]
                }
            }for row in rows]}
    return Response(json.dumps(response), mimetype="application/json")

if __name__ == '__main__':
    argv = sys.argv[1:]
    port = ''
    # command line arguments
    try:
        opts, args = getopt.getopt(argv, "p:", ["port="])
    except getopt.GetoptError:
        print('usage: backend.py -p {PORT_NUMBER}')
        sys.exit(2)
    if (len(opts) != 1):
        print('usage: backend.py -p {PORT_NUMBER}')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = str(arg)

    app.run(threaded=True, debug=False, host="0.0.0.0", port=int(port))
