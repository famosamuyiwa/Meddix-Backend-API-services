from werkzeug.security import safe_str_cmp as compare
from db import db
import sqlite3


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


    @classmethod
    def user(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        try:
            user = cls.find_by_username(username)
        except:
            return {"responseCode": -1, "message": "internal server error"}, 500

        query = "SELECT username, first_name, last_name from {} where username = ?;"
        
        if compare(user.category, "patient"):
            final_query = query.format("patients")
        if compare(user.category,"consultant"):
            final_query = query.format("consultants")
        if compare(user.category, "dispensary"):
            final_query = query.format("dispensary")

        result = cursor.execute(final_query,(username,))
        row = result.fetchone()
        connection.close()

        if row:
            user =  {
                        "responseCode": 0,
                        "username" : row[0],
                        "first_name" : row[1] ,
                        "last_name" : row [2],
                        "category" : user.category
                    }
            return user
 
        return {"responseCode": 1, "message" : "user not found"}, 400 

        
        


