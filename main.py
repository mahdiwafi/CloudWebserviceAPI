import random, string, json

from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

output = {}

parser = reqparse.RequestParser()
parser.add_argument('q', location='values')

class SimpleCalculatorQuery(Resource):

    def get(self):

        args = parser.parse_args()
        sentence = args['q']

        sentence = sentence.replace('\"', '')
        sentence = sentence.replace(' ', '+')

        score = eval(sentence)
        output["nilai"] = score

        return jsonify(output)

api.add_resource(SimpleCalculatorQuery, '/calculator/')

class SimpleCalculatorString(Resource):

    def get(self, calculate):
        return {"nilai": eval(calculate.replace('\"', ''))}

api.add_resource(SimpleCalculatorString, '/calculator/<string:calculate>')


class RandomNumber(Resource):

    def get(self, start, end):
        return {"random number": random.randrange(start, end+1)}

api.add_resource(RandomNumber, '/random/<int:start>/<int:end>')

temp_database = {"FREEGIFT100":{"used":False, "gems":100, "gold":100000, "exp":100},
                     "GAMEOFTHEYEAR":{"used":False, "gems":1000, "gold":1000000, "exp":1000},
                     "LA9C3RHPPHQH":{"used":False, "gems":60, "gold":0, "exp":50}}

class RedeemCoupon(Resource):
    
    def get(self, code):
        if(code in temp_database and temp_database[code]["used"] is False):
            temp_database[code]["used"]=True
            return {"status": "Success",
                "code": code}
        else:
            return {"status": "Failed",
                "code": code}

api.add_resource(RedeemCoupon, '/redeem/<string:code>')

class GenerateCoupon(Resource):
    
    def get(self, gems, gold, exp):
        
        code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        while (code in temp_database and temp_database[code]["used"] is False):
            code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

        temp_database[code] = {"used":False, "gems":gems, "gold":gold, "exp":exp}
        return {"status": "Success",
                "code": code}

api.add_resource(GenerateCoupon, '/generate/<int:gems>/<int:gold>/<int:exp>')

class ViewCoupon(Resource):
    
    def get(self, code=""):

        if(code in temp_database):
            return temp_database[code]
        else:
            return temp_database

api.add_resource(ViewCoupon, '/view/<string:code>', '/view')

class CustomCoupon(Resource):
    
    @app.route('/edit/<string:code>', methods = ['GET', 'POST', 'DELETE'])
    def post(code):
        if request.method == 'GET':
            return temp_database[code]
        if request.method == 'POST':
            data = request.form
            temp_database[code] = {"used":False, "gems":data["gems"], "gold":data["gold"], "exp":data["exp"]}
            return {"status": "Success",
                    "values": temp_database[code]}
        if request.method == 'DELETE':
            del temp_database[code]
            return temp_database
        else:
            return {"status": "Error",
                "code": 405}

api.add_resource(CustomCoupon, '/edit')

if __name__ == "__main__":
    app.run(debug=True)
