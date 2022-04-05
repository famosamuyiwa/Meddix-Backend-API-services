from flask_restful import Resource, reqparse
from statuses.paystatus import PaymentStatus
from models.prescription import PrescriptionModel
from models.consultant import ConsultantModel
from utils.utils import Utils
from datetime import datetime

class Prescription(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("patient_id")
    parser.add_argument("consultant_id")
    parser.add_argument("drug_name")
    parser.add_argument("serving")
    parser.add_argument("price")
    parser.add_argument("payment_status")


    def get(self, name):
        prescription = PrescriptionModel.find_by_id(name)

        if prescription:
            return {"responseCode": 0, "prescription": prescription.json()}, 201

        return {"responseCode": 1, "message": "record not found"}, 400

    def post(self, name):
        data = Prescription.parser.parse_args()
        rx = PrescriptionModel.find_by_aid(name)
        consultant = ConsultantModel.consultant(Utils.getCID(name))
    
        if rx:
            return {"responseCode" : 2, "message": "record already exists"},400 
        
        rx = PrescriptionModel(data['patient_id'], data['consultant_id'], name, data['drug_name'], data['serving'],  data['price'], datetime.date(datetime.now()), PaymentStatus.NA.value)
        consultant.total_prescriptions += 1

        try:
            rx.save_to_db()
            consultant.save_to_db()
        except:
            return {"responseCode": -1, "message": "internal server error"}, 500
        
        return rx.success()

    def put(self, name):
        data = Prescription.parser.parse_args()
        rx = PrescriptionModel.find_by_aid(name)

        
        if data['payment_status'] == PaymentStatus.CONFIRMED.value:
            rx.status = PaymentStatus.CONFIRMED.value
        
        try:
            rx.save_to_db()

        except:
            return {"responseCode": -1, "message": "internal server error"}, 500
        
        return rx.success()

class Prescriptions(Resource):

    def get(self,name):
        
        prescription = PrescriptionModel.find_by_pid(name)

        if prescription:
            return{"responseCode": 0, "prescriptions": [rx.json() for rx in PrescriptionModel.query.filter_by(patient_id = name).all()]}
        return {"responseCode": 1, "message": "record not found"}, 400

class AllPrescriptions(Resource):

    def get(self):
        
        return{"responseCode": 0, "prescriptions": [rx.json() for rx in PrescriptionModel.query.all()]}
        #return {"responseCode": 1, "message": "record not found"}, 400

               