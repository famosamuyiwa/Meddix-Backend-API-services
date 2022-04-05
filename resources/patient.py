from flask_restful import Resource, reqparse
from models.allergy import AllergyModel
from models.medicalrecord import VitalsModel, MedicalReportModel, MedicalRecordModel
from datetime import datetime


class Vitals(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument("height")
    parser.add_argument("weight")
    parser.add_argument("bmi")
    parser.add_argument("temperature")
    parser.add_argument("pulse")
    parser.add_argument("respiratory_rate")
    parser.add_argument("blood_pressure")
    parser.add_argument("blood_oxygen_saturation")


    def get(self, name):
        vitals = VitalsModel.find_by_id(name)
        if vitals:
            return vitals.json()
        return {"responseCode" : 1, "message": "record not found"}, 400

    def post(self,name):

        data = Vitals.parser.parse_args()

        vitals = VitalsModel.find_by_id(name)
        if vitals:
            return {"responseCode": 2, "message": "record already exists"}, 400
        
        vitals = VitalsModel(name, data['height'], data['weight'], data['bmi'], data['temperature'], data['pulse'], data['respiratory_rate'], data['blood_pressure'], data['blood_oxygen_saturation'], datetime.date(datetime.now()), datetime.date(datetime.now()))

        try:
            vitals.save_to_db()
        except:
            return {"responseCode": -1, "message": "internal server error"}, 500

        return vitals.success()


    def put(self, name):

        vitals = VitalsModel.find_by_id(name)

        data = Vitals.parser.parse_args()

        if vitals is None:
            vitals = VitalsModel(name, data['height'], data['weight'], data['bmi'], data['temperature'], data['pulse'], data['respiratory_rate'], data['blood_pressure'], data['blood_oxygen_saturation'], datetime.date(datetime.now()), datetime.date(datetime.now()))
       
        else:
            vitals.update_vitals(data['height'], data['weight'], data['bmi'], data['temperature'], data['pulse'], data['respiratory_rate'], data['blood_pressure'], data['blood_oxygen_saturation'], datetime.date(datetime.now()))
        
        try:
            vitals.save_to_db()
        except:
            return {"responseCode": -1, "message": "internal server error"}, 500
        
        return vitals.success()

class MedicalReport(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument("appointment_id")
    parser.add_argument("consultant_id")
    parser.add_argument("diagnosis")
   


    def get(self, name):
        medreport = MedicalReportModel.find_by_id(name)
        if medreport:
            return {"responseCode": 0, "report" : [report.json() for report in MedicalReportModel.query.filter_by(patient_id = name).all()]}
        return {"responseCode" : 1, "message": "record not found"}, 400

    def post(self, name):

        data = MedicalReport.parser.parse_args()

        medreport = MedicalReportModel(data["appointment_id"], name, data["consultant_id"], data["diagnosis"], datetime.date(datetime.now()))

        try:
            medreport.save_to_db()
        except:
            return {"responseCode": -1, "message": "internal server error"}, 500
        return medreport.success(), 201


class Allergy(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("allergy", required=True, help="supply what patient is allergic to")
    parser.add_argument("reaction")

    def post(self, name):
        data = Allergy.parser.parse_args()
        allergy = AllergyModel.find_by_id(name, data['allergy'])

        if allergy:
            return {"responseCode" : 2, "message": "record already exists"}
        
        allergy = AllergyModel(name, data['allergy'], data['reaction'], datetime.date(datetime.now()))

        try:
            allergy.save_to_db()
        except:
            return {"responseCode": -1, "message": "internal server error"}, 500

        return allergy.success()
        
    
    def delete(self, name):
        data = Allergy.parser.parse_args()
        
        allergy = AllergyModel.find_by_id(name, data['allergy'] )
        if allergy:
            try:
                allergy.delete_from_db()
            except:
                return {"responseCode": -1, "message": "internal server error"}, 500
            return {"responseCode": 0, "message": "allergy deleted successfully"}
        
        return {"responseCode": 1, "message": "record not found"}, 400



class Allergies(Resource):

    def get(self, name):        
        return {"allergies" : [allergy.json() for allergy in AllergyModel.query.filter_by(patient_id = name).all()]}

    


class MedicalRecord(Resource):

    def get(self, name):
        vitalsmodel = VitalsModel.find_by_id(name)
        vitals = vitalsmodel.json()
        
        allergies = [allergy.json() for allergy in AllergyModel.query.filter_by(patient_id=name).all()]
        diagnosis = [report.getDiagnosis() for report in MedicalReportModel.query.filter_by(patient_id=name).all()]
        visits = [report.visits() for report in MedicalReportModel.query.filter_by(patient_id=name).all()]
        
        medrecord = MedicalRecordModel(vitals, diagnosis, allergies, visits)
        

        if diagnosis:
            return medrecord.json()
        
        return {"responseCode" : 1, "message": "record not found"}, 400



























