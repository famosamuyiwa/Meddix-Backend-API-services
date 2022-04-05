from flask_apscheduler import APScheduler
from models.medicalrecord import MedicalReportModel
from statuses.apptstatus import ApptStatus
from db import db
from models.appointment import AppointmentModel
from datetime import datetime
from werkzeug.security import safe_str_cmp as compare

scheduler = APScheduler()


def report_update():
    app = scheduler.app
    with app.app_context():
        appt = AppointmentModel.query.all()
        for data in appt:
            try:
                if data.status.value == ApptStatus.COMPLETED.value:
                    report = MedicalReportModel(data.appointment_id, data.patient_id, data.consultant_id, data.diagnosis, datetime.date(datetime.now()))
                    data.status = ApptStatus.DONE.value
            except Exception as e:
                print(str(e))
            
            try:
              #  rx.save_to_db()
                report.save_to_db()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
    print("ok")




def test():
    app = scheduler.app
    with app.app_context():
        print("hello world")