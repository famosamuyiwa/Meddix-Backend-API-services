from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from models.user import UserModel


class ActiveUser(Resource):

    @jwt_required()
    def get(self):
        return {"message": "not available yet"}, 200 #UserModel.user(current_identity.username)    

