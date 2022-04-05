from models.user import UserModel
from werkzeug.security import safe_str_cmp as compare
from flask import request



def authenticate(username, password): #authenticates jwt_token
    user = UserModel.find_by_username(username)
    if user and compare(user.password, password):
        return user

def identity(payload):    #verifies jwt_token user
    user_id = payload['identity']
    return UserModel.find_by_id(user_id) 