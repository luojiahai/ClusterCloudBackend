from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from schedule import *

app = Flask(__name__)
api = Api(app)

connect_parser = reqparse.RequestParser()
connect_parser.add_argument('ip')
connect_parser.add_argument('port')

schedule_parser = reqparse.RequestParser()
schedule_parser.add_argument('ids')

class Connect(Resource):
    def get(self):
        return workers

    def post(self):
        args = connect_parser.parse_args()
        if (hasWorker(args['ip'])):
            return "EXISTED"
        else:
            addWorker(args)
            return "OK"

class Schedule(Resource):
    def post(self):
        args = parser.parse_args()
        if (hasWorker(args['ip'])):
            return "EXISTED"
        else:
            addWorker(args)
            return "OK"

api.add_resource(Connect, '/api/connect')
api.add_resource(Schedule, '/api/schedule')

if __name__ == '__main__':
    app.run(debug=True)

