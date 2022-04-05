from statuses.paystatus import PaymentStatus
from db import db

class PrescriptionModel(db.Model):

    __tablename__ = "prescriptions"

    id = db.Column(db.Integer(), primary_key=True)
    patient_id = db.Column(db.Integer())
    consultant_id = db.Column(db.Integer())
    appointment_id = db.Column(db.Integer())
    drug_name = db.Column(db.String())
    serving = db.Column(db.Integer())
    prescription_id = db.Column(db.String())
    price = db.Column(db.Integer())
    create_date = db.Column(db.String())
    status = db.Column(db.Enum(PaymentStatus, name='status', default=PaymentStatus.INITIATED))    

    def __init__(self, pid, cid, appt_id, drug, serving, price, date, status):

        self.patient_id = pid
        self.consultant_id = cid
        self.appointment_id = appt_id
        self.drug_name = drug
        self.serving = serving
        self.price = price
        self.prescription_id = "RX"+"-"+str(cid)+"-"+str(pid)+"-"+str(date)
        self.create_date = date
        self.status = status

    @classmethod
    def find_by_id(cls, rx_id):
        return cls.query.filter_by(prescription_id = rx_id).first()
    
    @classmethod
    def find_by_pid(cls, pid):
        return cls.query.filter_by(patient_id = pid).first()
    

    @classmethod
    def find_by_aid(cls, appt_id):
        return cls.query.filter_by(appointment_id = appt_id).first()

    
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        

  


    def json(self):
        return {
            "patient_id" : self.patient_id,
            "consultant_id": self.consultant_id,
            "appointment_id": self.appointment_id,
            "drug_name": self.drug_name,
            "serving": self.serving,
            "price": self.price,
            "prescription_id": self.prescription_id,
            "status" : self.status.value
        }

    def success(self):
        return {"responseCode": 0, "message": "prescription saved successfully"}

    @classmethod
    def find_by_appointment(cls, appt_id):
        return cls.query.filter_by(appointment_id = appt_id).first()

    


