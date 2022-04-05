# data analysis and wrangling
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
import os
import json

def format(data):
    return data.split(",")
    

def map_disease(diseases):
    prognosis = {"prognosis": {disease : diseases.index(disease) for disease in diseases}}
    return prognosis

def prediction(data):
    for i in range(0,len(symptoms)):
        for k in data:
            if(k==symptoms[i]):
                result[i] = 1
                
    labels = [result]

    print(labels)
    predict = tree.predict(labels)
    
    predicted=predict[0]
        
    done = 'no'
    for a in range(0,len(disease)):
        if(predicted == a):
            done = 'yes'
            break
            
    if (done == 'yes'):
        return disease[a]
    else:
        return None

def get_specialist(disease):
    return json_data[disease]


cwd = os.getcwd()
print("My current working directory is: {} ".format(cwd))
file_train = os.path.join(cwd, "symptomChecker/Training.csv")
file_test = os.path.join(cwd, "symptomChecker/Testing.csv")
f = open(os.path.join(cwd,"symptomChecker/disease-specialist.json"),)
json_data = json.load(f)


train = pd.read_csv(file_train)
test = pd.read_csv(file_test)

train.head()

columns = train.columns.values[:132]
symptoms = columns.tolist()


disease = ['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction',
'Peptic ulcer diseae','AIDS','Diabetes ','Gastroenteritis','Bronchial Asthma','Hypertension ',
'Migraine','Cervical spondylosis',
'Paralysis (brain hemorrhage)','Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A',
'Hepatitis B','Hepatitis C','Hepatitis D','Hepatitis E','Alcoholic hepatitis','Tuberculosis',
'Common Cold','Pneumonia','Dimorphic hemmorhoids(piles)',
'Heart attack','Varicose veins','Hypothyroidism','Hyperthyroidism','Hypoglycemia','Osteoarthristis',
'Arthritis','(vertigo) Paroymsal  Positional Vertigo','Acne','Urinary tract infection','Psoriasis',
'Impetigo']

result=[]
for i in range(0,len(symptoms)):
    result.append(0)




train.replace(map_disease(disease), inplace=True)
X_train = train[symptoms]
y_train = train[["prognosis"]]
np.ravel(y_train)

test.replace(map_disease(disease), inplace=True)
X_test = test[symptoms]
y_test = test[["prognosis"]]
np.ravel(y_test)

tree = DecisionTreeClassifier().fit(X_train, y_train)

print(f' Train score: {tree.score(X_train, y_train) * 100} %')
print(f' Test score: {tree.score(X_test, y_test) * 100} %')

tree_predict = tree.predict(X_test)


print(f'accuracy_score: {round(accuracy_score(y_test, tree_predict *100),2)} %')







