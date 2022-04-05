from flask_restful import Resource, reqparse
from models.activities import ActivityModel
from statuses.apptstatus import ApptStatus
from models.appointment import AppointmentModel
from models.consultant import ConsultantModel
from models.patient import PatientModel
from utils.utils import Utils
from datetime import datetime
from werkzeug.security import safe_str_cmp as compare

class Appointment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("consultant_id")
    parser.add_argument("date")
    parser.add_argument("time")
    parser.add_argument("venue")
    parser.add_argument("reason")
    parser.add_argument("patient_id")
    parser.add_argument("status")
    parser.add_argument("diagnosis")
    
    def get(self, name):
        try:
            appointment = AppointmentModel.find_by_id(name)
            return appointment.json()
        except:
            return {"responseCode": 1, "message": "record not found"}, 400

    def post(self, name):
        data = Appointment.parser.parse_args()
        cons = ConsultantModel.consultant(data['consultant_id'])
        pat = PatientModel.patient(data['patient_id'])
        
        if AppointmentModel.find_by_id("APPT"+"-"+str(data['consultant_id'])+"-"+str(data['patient_id'])+"-"+str(datetime.date(datetime.now()))):
            return {"responseCode": 2, "message": "appointment already exists"}, 400

        appointment = AppointmentModel(data['consultant_id'], data['patient_id'], datetime.date(datetime.now()), datetime.date(datetime.now()), data['date'], data['time'], data['venue'], data['reason'], ApptStatus.PENDING.value, "None")
        activity = ActivityModel(pat.user_id, "Appointment request initiated with Dr. "+cons.last_name, str(datetime.date(datetime.now())),  str(datetime.time(datetime.now())) )

        try:
            appointment.save_to_db()
            activity.save_to_db()
        except:
            return {"responseCode": 5,"message": "an error occured while adding appointment"}, 500
        
        return appointment.success()

    def put(self, name):
        
        appointment = AppointmentModel.find_by_id(name)
        consultant = ConsultantModel.consultant(Utils.getCID(name))
        patient = PatientModel.patient(Utils.getPID(name))

        data = Appointment.parser.parse_args()

        if appointment is None:
            appointment = AppointmentModel(data['consultant_id'], data['patient_id'], datetime.date(datetime.now()), datetime.date(datetime.now()), data['date'], data['time'], data['venue'], data['reason'], ApptStatus.PENDING.value, "None")
            activity = ActivityModel(patient.user_id, "Appointment request initiated with Dr. "+consultant.last_name, str(datetime.date(datetime.now())),  str(datetime.time(datetime.now())) )

        elif appointment.status.value == ApptStatus.DONE.value:
            return{"responseCode": -3, "message": "bad request"}, 400
        
        else:
            if data['status'] == ApptStatus.RESCHEDULED.value:
                appointment.reschedule(datetime.date(datetime.now()), data['date'], data['time'])
                activity = ActivityModel(patient.user_id, "Appointment Reschedule Request initiated with Dr. "+consultant.last_name, str(datetime.date(datetime.now())),  str(datetime.time(datetime.now())) )

            if data['status'] == ApptStatus.COMPLETED.value:
                appointment.diagnosis = data['diagnosis']
                appointment.status = ApptStatus.COMPLETED.value
                consultant.appointments_completed += 1
                activity = ActivityModel(consultant.user_id, "Appointment #"+name+" marked as completed", str(datetime.date(datetime.now())),  str(datetime.time(datetime.now())) )

            if data['status'] == ApptStatus.SCHEDULED.value:
                appointment.status = ApptStatus.SCHEDULED.value
          #      activity = ActivityModel(consultant.user_id, "Appointment Request #"+name+" approved successfully", str(datetime.date(datetime.now())),  str(datetime.time(datetime.now())) )

            if data['status'] == ApptStatus.PENDING.value:
                appointment.scheduled(datetime.date(datetime.now()), data['date'], data['time'], data['venue'])
                activity = ActivityModel(consultant.user_id, "Appointment Request #"+name+" approved successfully", str(datetime.date(datetime.now())),  str(datetime.time(datetime.now())) )


        try:
            appointment.save_to_db()
            consultant.save_to_db()
            activity.save_to_db()
        except:
            return {"responseCode": 5,"message": "an error occured while adding appointment"}, 500
 
        return appointment.success()


    def delete(self, name):
        appointment = AppointmentModel.find_by_id(name)
        if appointment:
            appointment.delete_from_db()
            return {"responseCode": 0, "message": "appointment deleted"}, 201

        return {"responseCode": 1, "message": "record not found"}, 400

class Appointments(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("category", required=True)
    parser.add_argument("id", required=True)

    def get(self):
        data = Appointments.parser.parse_args()

        if compare(data['category'], "consultant"):
            return {"responseCode": 0, "appointments": [appointment.json("None",str(PatientModel.patient(appointment.patient_id).last_name) + " " +str(PatientModel.patient(appointment.patient_id).first_name)) for appointment in AppointmentModel.query.filter_by(consultant_id=data['id']).all()]}, 201

        elif compare(data['category'], "patient"):
            return {"responseCode": 0, "appointments": [appointment.json(str(ConsultantModel.consultant(appointment.consultant_id).last_name) + " " +str(ConsultantModel.consultant(appointment.consultant_id).first_name), "None") for appointment in AppointmentModel.query.filter_by(patient_id=data['id']).all()]}, 201

        else:
            return {"responseCode": -3, "message": "user type does not exist"}, 400
#
