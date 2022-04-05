from db import db


class PatientModel(db.Model):
    
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    other_name = db.Column(db.String(80))
    mobile_number = db.Column(db.Integer())
    email = db.Column(db.String(80))
    user_id = db.Column(db.Integer())

    def __init__(self, pid, firstname, lastname, othername, mobile_number, email):
        self.patient_id = pid
        self.first_name = firstname
        self.last_name = lastname
        self.other_name = othername
        self.mobile_number = mobile_number
        self.email = email


    @classmethod
    def patient(cls, pid):
        return cls.query.filter_by(patient_id=pid).first()

    def patients(cls):
        return cls.query

    def json(self):
        patient =  {
                        "responseCode": 0,
                        "consultant_id": self.consultant_id,
                        "first_name" : self.first_name,
                        "last_name" : self.last_name,
                        "other_name" : self.other_name,
                        "mobile_number": "0{}".format(self.mobile_number),
                        "email" : self.email 
                        }

        return patient
