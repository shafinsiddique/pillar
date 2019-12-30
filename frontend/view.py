from flask import Flask,render_template
import requests
app = Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    patients = requests.get("https://pillarrestapi.herokuapp.com/patients/").json()
    for x in range(len(patients)):
        if (patients[x]['medicalRecord']):
            patients[x]['lastVisit'] = patients[x]['medicalRecord'][-1]['date']

        else:
            patients[x]['lastVisit'] = "-"
    return render_template('index.html',patients=patients)

@app.route('/<patientName>',methods=['GET'])
def patient(patientName):
    print(requests.get("https://pillarrestapi.herokuapp.com/sPatient/" + patientName).json())
    return render_template('patient.html')
