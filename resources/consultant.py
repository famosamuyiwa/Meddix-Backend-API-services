from flask_restful import Resource, reqparse
from models.consultant import ConsultantModel

class Consultant(Resource):

    def get(self, name):

        consultant =  ConsultantModel.consultant(name)
        return consultant.json()

class ConsultantList(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("specialty", required = True)
        data = parser.parse_args()
        return {"responseCode": 0, "consultants": [consultants.json() for consultants in ConsultantModel.query.filter_by(specialty=data['specialty']).all()]}