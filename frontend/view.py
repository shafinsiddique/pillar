from flask import Flask,render_template,request,flash
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

@app.route('/<patientName>',methods=['GET','POST'])
def patient(patientName):
    pInfo =requests.get("https://pillarrestapi.herokuapp.com/sPatient/" + patientName).json()
    if request.method == "GET":
        return render_template('patient.html',info=pInfo)

    requests.post("https://pillarrestapi.herokuapp.com/sendNote",
                  data={"note":request.form['note'],"pin": pInfo['pin'],
                        "phone":pInfo['phone']})


    return render_template('patient.html',info=pInfo)