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

@app.route("/get1")
def get1():
    rows = db.view("test-doc/new-view-01")
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
                    "polarity": row.value
                }
            }
        response["features"].append(feature)
    return Response(json.dumps(response), mimetype="application/json")

@app.route("/get2")
def get2():
    rows = db.view("test-doc/new-view-02")
    response = []
    for row in rows:
        obj = {
                "hashtag": row.key,
                "count": row.value
            }
        response.append(obj)
    return Response(json.dumps(response), mimetype="application/json")

if __name__ == '__main__':
    app.run(threaded=True, debug=False, host="115.146.95.53", port=4000)
