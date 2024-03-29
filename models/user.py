from werkzeug.security import safe_str_cmp as compare
from db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(80))
    category = db.Column(db.String(30))

    def __init__(self, _id, username, password, category):
        self.id = _id
        self.username = username
        self.password = password
        self.category = category
    
    def __str__(self):
        return '%s' % self.username
     

    @classmethod
    def find_by_username(cls, username):
       return cls.query.filter_by(username=username).first()
    
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()



        
        


