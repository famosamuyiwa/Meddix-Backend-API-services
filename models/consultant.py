from db import db


class ConsultantModel(db.Model):
    
    __tablename__ = "consultants"
    __table_args__ = {'extend_existing':True}

    consultant_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    other_name = db.Column(db.String(80))
    specialty = db.Column(db.String(80))
    mobile_number = db.Column(db.String(80))
    email = db.Column(db.String(80))
    total_prescriptions = db.Column(db.Integer())
    appointments_completed = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    username = db.Column(db.String(80))
    gender = db.Column(db.String(1))
    create_date = db.Column(db.String(80))
    

    def __init__(self, cid, firstname, lastname, othername, specialty, mobile_number, email, total_rx, appts_completed):
        self.consultant_id = cid
        self.first_name = firstname
        self.last_name = lastname
        self.other_name = othername
        self.specialty = specialty
        self.mobile_number = mobile_number
        self.email = email
        self.appointments_completed = appts_completed
        self.total_prescriptions = total_rx

    @classmethod
    def consultant(cls, cid):
        return cls.query.filter_by(consultant_id=cid).first()

    def consultants(cls):
        return cls.query
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        consultant =  {
                        "responseCode": 0,
                        "consultant_id": self.consultant_id,
                        "first_name" : self.first_name,
                        "last_name" : self.last_name,
                        "other_name" : self.other_name,
                        "specialty" : self.specialty,
                        "mobile_number": "0{}".format(self.mobile_number),
                        "email" : self.email,
                        "total_prescriptions" : self.total_prescriptions,
                        "appointments_completed" : self.appointments_completed  
                        }

        return consultant
