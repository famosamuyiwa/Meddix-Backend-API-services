from flask_restful import Resource, reqparse
from models.symptomChecker import prediction, format, get_specialist

class SymptomChecker(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument("symptoms", required=True, help="supply symptoms separated by a comma")

    def get(self):
        data = SymptomChecker.parser.parse_args()
        prognosis = prediction(format(data['symptoms']))
        specialist = get_specialist(prognosis)

        return {"prognosis": prognosis, "specialist": specialist}, 201


