from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from resources.activities import Activity, Activities
from security import authenticate, identity
from resources.basicData import BasicData
from resources.user import ActiveUser
from resources.consultant import Consultant, ConsultantList
from resources.appointment import Appointment, Appointments
from resources.patient import Vitals, MedicalReport, MedicalRecord, Allergies, Allergy
from resources.symptomChecker import SymptomChecker
from resources.prescription import Prescription, Prescriptions, AllPrescriptions
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import json

f = open("data.json",)
data = json.load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'         #set database for SQLALCHEMY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         
app.secret_key = data['key']                        #get key from data.json
api = Api(app)



jwt = JWT(app, authenticate, identity) # /auth

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'user_id': identity.id,
                        'logged_in': True,
                        'category': identity.category
                   })

api.add_resource(BasicData, '/basicdata/<string:name>')   #http://127.0.0.1:5000/Patient/Famosa
api.add_resource(ActiveUser, '/active-user')
api.add_resource(Consultant, '/consultant/<string:name>')
api.add_resource(ConsultantList, '/consultants')
api.add_resource(Appointment, '/appointment/<string:name>')
api.add_resource(Appointments, '/appointments')
api.add_resource(Vitals, '/medical-record/vitals/<string:name>')
api.add_resource(MedicalReport, '/medical-record/report/<string:name>')
api.add_resource(MedicalRecord, '/medical-record/<string:name>')
api.add_resource(SymptomChecker, '/symptom-checker')
api.add_resource(Prescription, '/prescription/<string:name>')
api.add_resource(Prescriptions, '/prescriptions/<string:name>')
api.add_resource(AllPrescriptions, '/prescriptions')
api.add_resource(Allergy, '/allergy/<string:name>')
api.add_resource(Allergies, '/allergies/<string:name>')
api.add_resource(Activity, '/activity/<string:name>')
api.add_resource(Activities, '/activities/<string:name>')



@app.after_request
def after_request(response):
  response.headers.set('Access-Control-Allow-Origin', '/')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.set('Access-Control-Allow-Credentials', True)
  return response 


class Config(object):
    
    JOBS = [
        {
            'id': 'report_update',
            'func': 'tasks:report_update',
            'trigger': 'interval',
            'minutes': 1, # call the task function every 1 minute
            'replace_existing': True
        }
    ]
    JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///data.db')
    }
    SCHEDULER_API_ENABLED = True

    

if __name__ == '__main__':  #run only if app.py is launched and not called from another class
    from flask_apscheduler import APScheduler
    from tasks import scheduler
    from db import db
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    db.init_app(app)
    app.run(port=5500, debug=True)