from db import db
from datetime import datetime

class VitalsModel(db.Model):

    __tablename__ = "vitals"

    id = db.Column(db.Integer, primary_key = True)
    patient_id= db.Column(db.Integer())
    height= db.Column(db.Integer())
    weight = db.Column(db.Integer())
    bmi = db.Column(db.Integer())
    temperature= db.Column(db.Integer())
    pulse= db.Column(db.Integer()) 
    respiratory_rate = db.Column(db.Integer())
    blood_pressure = db.Column(db.String())
    blood_oxygen_saturation = db.Column(db.Integer())
    create_date = db.Column(db.String())
    last_modified_date= db.Column(db.String())

    def __init__(self, pid, height, weight, bmi, temperature, pulse, resp_rate, bp, b_o_s, create_date, l_m_d):

        self.patient_id = pid
        self.height = height
        self.weight = weight
        self.bmi = bmi
        self.temperature = temperature
        self.pulse = pulse
        self.respiratory_rate = resp_rate
        self.blood_pressure = bp
        self.blood_oxygen_saturation = b_o_s
        self.create_date = create_date
        self.last_modified_date = l_m_d

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_vitals(self, height, weight, bmi, temperature, pulse, resp_rate, bp, b_o_s, l_m_d):
        self.height = height
        self.weight = weight
        self.bmi = bmi
        self.temperature = temperature
        self.pulse = pulse
        self.respiratory_rate = resp_rate
        self.blood_pressure = bp
        self.blood_oxygen_saturation = b_o_s
        self.last_modified_date = l_m_d

    def success(self):
        return {"responseCode": 0, "message": "vitals updated successfully"}

    def json(self):
        x = datetime.strptime(self.last_modified_date, "%Y-%m-%d").strftime('%B %d %Y')
        y = x.split(" ")
        z = VitalsModel.make_ordinal(int(y[1]))
        last_checked = y[0] + " " + z + ", "+ y[2]
        return {
                "patient_id" :  self.patient_id, 
                "height": self.height ,
                "weight" : self.weight ,
                "bmi" : self.bmi ,
                "temperature": self.temperature ,
                "pulse" : self.pulse ,
                "respiratory_rate" : self.respiratory_rate ,
                "blood_pressure" : self.blood_pressure,
                "blood_oxygen_saturation" : self.blood_oxygen_saturation,
                "last_checked": last_checked
            }
    
    def make_ordinal(n):
        '''
        Convert an integer into its ordinal representation::
            e.g:
            make_ordinal(3)   => '3rd'
        '''
        n = int(n)
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        return str(n) + suffix

    @classmethod
    def find_by_id(cls, pid):
        return cls.query.filter_by(patient_id = pid).first()

class MedicalReportModel(db.Model):

    __tablename__ = "medical_report"

    id = db.Column(db.Integer(), primary_key = True)
    appointment_id = db.Column(db.Integer())
    patient_id = db.Column(db.Integer())
    consultant_id = db.Column(db.Integer())
    diagnosis = db.Column(db.String())
    create_date = db.Column(db.String())

    def __init__(self, appt_id, pid, cid, diagnosis, create_date):
        self.appointment_id = appt_id
        self.patient_id = pid
        self.consultant_id = cid
        self.diagnosis = diagnosis
        self.create_date = create_date

    @classmethod
    def find_by_id(cls, pid):
        return cls.query.filter_by(patient_id = pid).first()

    @classmethod
    def find_by_appointment(cls, appt):
        return cls.query.filter_by(appointment_id = appt).first()

    def save_to_db(self):
        db.session.add(self)
        

    def json(self):
        return {
                "appointment_id": self.appointment_id,
                "patient_id": self.patient_id,
                "consultant_id": self.consultant_id,
                "diagnosis": self.diagnosis
        }

    def getDiagnosis(self):
        return {"diagnosis" : self.diagnosis}

    def visits(self):
        return {"visits": self.create_date}

    def success(self):
        return {"responseCode": 0, "message" : "report updated successfully"}
    
    def pid(self):
        return self.patient_id
    
    def cid(self):
        return self.consultant_id

class MedicalRecordModel():

    def __init__(self, vitals, diagnosis, allergies, visits):
        self.vitals = vitals
        self.diagnosis = diagnosis
        self.allergies = allergies
        self.visits = visits

    def json(self):
        return {
            "vitals": self.vitals,
            "diagnosis": self.diagnosis,
            "allergies": self.allergies,
            "visits": self.visits
        }
    