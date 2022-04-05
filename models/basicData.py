from db import db
import sqlite3
class BasicDataModel():

    def patientData(patientID):
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "SELECT * FROM patients WHERE user_id = ?;"
            result = cursor.execute(query, (patientID,))
            row = result.fetchone()

            connection.close()
            if row:
                return {
                        'responseCode': 0,
                        'patient': {
                                    'patient_id' : row[0], 
                                    'first_name' : row[1],
                                    'last_name' : row[2],
                                    'other_name': row[13],
                                    'username' : row[3],
                                    'portrait' : row[4],
                                    'gender' : row[5],
                                    'mobile_number' : "0{}".format(row[8]),
                                    'home_address' : row[9],
                                    'email' : row[11],
                                    'age' : row[16]
                                    }
                        }
            return {'responseCode': 1, 'message': 'user not found'}, 400
                

    def consultantData(consultantID):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
           
        query = "SELECT * FROM consultants WHERE user_id = ?;"
        result = connection.execute(query,(consultantID,))
        
        row = result.fetchone()

        connection.close()

        if row:
            return{
                    'responseCode': 0,
                    'consultant': {
                        'consultant_id': row[0],
                        'first_name': row[1],
                        'last_name': row[2],
                        'other_name' : row[13],
                        'username': row[3],
                        'gender': row[4],
                        'specialty': row[5],
                        'mobile_number': "0{}".format(row[7]),
                        'home_address': row[8],
                        'status': row[9],
                        'email': row[10],
                        "total_prescriptions" : row[15],
                        "appointments_completed" : row[14]  
                    }
            }
        return {'responseCode': 1, 'message': 'user not found'}, 400


    def dispensaryData(dispensaryID):
         
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM dispensary WHERE user_id = ?"
        result = cursor.execute(query, (dispensaryID,))

        row = result.fetchone()
        
        if row:
            return{
                    'responseCode': 0,
                    'dispensary': {
                        'dispensary_id': row[0],
                        'first_name': row[1],
                        'last_name': row[2],
                        'username': row[3],
                        'gender': row[4],
                        'mobile_number': "0{}".format(row[6]),
                        'home_address': row[7],
                        'status': row[8],
                        'email': row[9]
                    }
            }
        return {'responseCode': 1, 'message': 'user not found'}, 400