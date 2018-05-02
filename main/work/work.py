from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

scheduler = ""

parser = reqparse.RequestParser()
parser.add_argument('ip')
parser.add_argument('port')

class Connect(Resource):
    def get(self):
        return workers

    def post(self):
        args = parser.parse_args()
        if (args['ip'] in workers):
            return "EXISTED"
        else:
            workers[args['ip']] = {'port': args['port']}
            return "OK"

api.add_resource(Connect, '/connect')

if __name__ == '__main__':
    app.run(debug=True)