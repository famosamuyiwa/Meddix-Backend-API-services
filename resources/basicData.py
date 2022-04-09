from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp as compare
from models.basicData import PatientDataModel, ConsultantDataModel, DispenserDataModel



class BasicData(Resource):
    
    @jwt_required()
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("category", required = True, help="supply user category")
        data = parser.parse_args()

        if compare(data['category'], "patient"):        #safe string compare (safe_str_cmp) as compare 
            patient = PatientDataModel.patient(name)
            return patient.json()
        
        if compare(data['category'], "consultant"):
            consultant = ConsultantDataModel.consultant(name)
            return consultant.json()

        if compare(data['category'], "dispenser"):
            dispenser = DispenserDataModel.dispenser(name)
            return dispenser.json()
        
        return {"responseCode": 1, "message" : "user type {data[category]} does not exist".format(data['category'])}, 400

        

       


