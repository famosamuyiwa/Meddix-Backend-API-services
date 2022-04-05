from db import db

class ActivityModel(db.Model):
      
    __tablename__ = "client_activity_log"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    activity = db.Column(db.String(80))
    create_date = db.Column(db.String(80))
    time_stamp = db.Column(db.String(80))
    

    def __init__(self, user_id, activity, create_date, time_stamp):
        self.user_id = user_id
        self.activity = activity
        self.create_date = create_date
        self.time_stamp = time_stamp

    @classmethod
    def find_by_userid(cls, uid):
        return cls.query.filter_by(user_id=uid).all()

     
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
          
    def json(self):
        return {
            "user_id" : self.user_id,
            "activity": self.activity,
            "create_date": self.create_date,
            "time_stamp": self.time_stamp
        }

    
    def success(self):
        return {"responseCode": 0, "message": "activity saved successfully"}