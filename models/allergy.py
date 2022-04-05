from db import db

class AllergyModel(db.Model):

    __tablename__ = "allergies"

    id = db.Column(db.Integer(), primary_key=True)
    patient_id = db.Column(db.Integer())
    allergy = db.Column(db.String())
    reaction = db.Column(db.String())
    create_date = db.Column(db.String())

    def __init__(self, pid, allergy, reaction, create_date):
        self.patient_id = pid
        self.allergy = allergy
        self.reaction = reaction
        self.create_date = create_date

    @classmethod
    def find_by_id(cls, pid, allergy):
        return cls.query.filter_by(patient_id = pid, allergy = allergy).first()
    
    def json(self):
        return{
            "allergy": self.allergy,
            "reaction": self.reaction
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def success(self):
        return {
            "responseCode": 0,
            "message": "allergy saved succesfully"
        }
