from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from werkzeug.security import safe_str_cmp as compare
from models.user import UserModel


class ActiveUser(Resource):

    @jwt_required()
    def get(self):
        return UserModel.user(current_identity.username)    

