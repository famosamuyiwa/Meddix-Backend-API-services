from db import db

class PatientDataModel(db.Model):

    __tablename__ = "patients"

    patient_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    other_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    gender = db.Column(db.String(1))
    mobile_number = db.Column(db.Integer())
    home_address = db.Column(db.String(80))
    email = db.Column(db.String(80))
    age = db.Column(db.Integer())

    def __init__(self,pid,fname,lname,oname,username,gender,mobile_number,home_address,email,age):
        self.patient_id = pid
        self.first_name = fname
        self.last_name = lname
        self.other_name = oname
        self.username = username
        self.gender = gender
        self.mobile_number = mobile_number
        self.home_address = home_address
        self.email = email
        self.age = age

    @classmethod
    def patient(cls, pid):
        return cls.query.filter_by(patient_id=pid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def json(self):
        basicdata =  {
                        "responseCode": 0,
                        "patient_id": self.patient_id,
                        "first_name" : self.first_name,
                        "last_name" : self.last_name,
                        "other_name" : self.other_name,
                        "username" : self.username,
                        "mobile_number": "0{}".format(self.mobile_number),
                        "email" : self.email,
                        "age" : self.age,
                        "gender": self.gender,
                        "home_address": self.home_address
                        }

        return basicdata

    
class ConsultantDataModel(db.Model):
    
    __tablename__ = "consultants"

    consultant_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    other_name = db.Column(db.String(50))
    specialty = db.Column(db.String(50))
    mobile_number = db.Column(db.Integer())
    email = db.Column(db.String(50))
    total_prescriptions = db.Column(db.Integer())
    appointments_completed = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    username = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    create_date = db.Column(db.String(50))
    
    @classmethod
    def consultant(cls, cid):
        return cls.query.filter_by(consultant_id=cid).first()


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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        basicdata =  {
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

        return basicdata
    
class DispenserDataModel(db.Model):
         
    __tablename__ = "dispensary"
    dispensary_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    mobile_number = db.Column(db.Integer())
    email = db.Column(db.String(50))
    user_id = db.Column(db.Integer())
    username = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    create_date = db.Column(db.String(50))
    home_address = db.Column(db.String(80))

    @classmethod
    def dispenser(cls, did):
        return cls.query.filter_by(dispensary_id=did).first()


    def __init__(self, fname, lname, username, gender, create_date, mobile_number, home_address, status, email, user_id):
        self.first_name = fname
        self.last_name = lname
        self.username = username
        self.gender = gender
        self.create_date = create_date
        self.mobile_number = mobile_number
        self.home_address = home_address
        self.status = status
        self.email = email
        self.user_id = user_id

    def json(self):
        basicdata =  {
                    "responseCode": 0,
                    "dispensary_id": self.dispensary_id,
                    "first_name" : self.first_name,
                    "last_name" : self.last_name,
                    "mobile_number": "0{}".format(self.mobile_number),
                    "email" : self.email,
                    }

        return basicdata