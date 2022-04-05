from flask_restful import Resource,reqparse
from models.activities import ActivityModel
from datetime import datetime

class Activity(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("status")

    def post(self, name):

        data = Activity.parser.parse_args()
        activity = ActivityModel(name, data['status'], str(datetime.date(datetime.now())),  str(datetime.time(datetime.now())) )


        try:
            activity.save_to_db()
        except:
            return {"responseCode": -1, "message": "internal server error"}, 500
        
        return activity.success()


class Activities(Resource):

    def get(self, name):
        return {"responseCode": 0, "activity": [activity.json() for activity in ActivityModel.query.filter_by(user_id=name).all()]}

    