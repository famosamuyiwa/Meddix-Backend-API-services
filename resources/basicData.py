from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp as compare
from models.basicData import BasicDataModel



class BasicData(Resource):
    
    @jwt_required()
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("category", required = True, help="supply user category")
        data = parser.parse_args()

        if compare(data['category'], "patient"):        #safe string compare (safe_str_cmp) as compare 
            return BasicDataModel.patientData(name)
        
        if compare(data['category'], "consultant"):
            return BasicDataModel.consultantData(name)

        if compare(data['category'], "dispenser"):
            return BasicDataModel.dispensaryData(name)
        
        return {"responseCode": 1, "message" : "user type '%s' does not exist".format(data['category'])}, 400

        

       


