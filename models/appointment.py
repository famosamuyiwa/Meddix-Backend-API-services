from statuses.apptstatus import ApptStatus
from db import db

class AppointmentModel(db.Model):

    __tablename__ = "appointments"
    
    id = db.Column(db.Integer(), primary_key=True)
    consultant_id = db.Column(db.Integer(), nullable=False)
    patient_id = db.Column(db.Integer())
    create_date = db.Column(db.String(80))
    last_modified_date = db.Column(db.String(80))
    schedule_date = db.Column(db.String(80))
    schedule_time = db.Column(db.String(80))
    schedule_venue = db.Column(db.String(80))
    schedule_reason = db.Column(db.String(80))
    status = db.Column(db.Enum(ApptStatus, name='status', default=ApptStatus.PENDING))    
    appointment_id = db.Column(db.String(80))
    diagnosis = db.Column(db.String(80))


    def __init__(self, cid, pid, create_date, last_modified_date, date, time, venue, reason, status, diagnosis):
        self.consultant_id = cid
        self.patient_id = pid
        self.create_date = create_date
        self.last_modified_date = last_modified_date
        self.schedule_date = date
        self.schedule_time = time
        self.schedule_venue = venue
        self.schedule_reason = reason
        self.status = status
        self.appointment_id = "APPT"+"-"+str(cid)+"-"+str(pid)+"-"+str(create_date)
        self.diagnosis = diagnosis

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    
    def reschedule(self, l_m_date, date, time):
        self.last_modified_date = l_m_date
        self.schedule_date = date
        self.schedule_time = time
        self.status = ApptStatus.PENDING.value
    
 

    def scheduled(self, l_m_date, date, time, venue):
        self.last_modified_date = l_m_date
        self.schedule_date = date
        self.schedule_time = time
        self.schedule_venue = venue 
        self.status = ApptStatus.SCHEDULED.value

    def diagnosed(self, diagnosis):
        self.diagnosis = diagnosis    


    @classmethod
    def find_by_id(cls, appt_id):
        return cls.query.filter_by(appointment_id = appt_id).first()

    def success(self):
        return {"responseCode": 0, "message": "appointment has been saved to database"}

    def json(self, cname, pname):
        appointment = {
                        "consultant_id" : self.consultant_id,
                        "patient_id" : self.patient_id,
                        "consultant_name": cname,
                        "patient_name": pname,
                        "schedule_date": self.schedule_date,
                        "schedule_time" : self.schedule_time,
                        "schedule_venue": self.schedule_venue,
                        "schedule_reason" : self.schedule_reason,
                        "status" : self.status.value,
                        "appointment_id" : self.appointment_id 
                    }      
        return appointment  

    def pid(self):
        return self.patient_id
    
    def cid(self):
        return self.consultant_id
    
    