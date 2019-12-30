from flask import Flask, request, jsonify, Response
from dbHelper import PatientDBHelper, DoctorNotesHelper, DispenseDBHelper
from summarizer import summarize
from face_rekog import face_eval
from flask import render_template
from flask_cors import CORS
from sms import sendText
from twilio.twiml.voice_response import VoiceResponse,Gather

app = Flask(__name__)
CORS(app)

@app.route("/",methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/summarize/', methods=['GET', 'POST'])
def summarizer():
    if request.method == 'POST':
        data = request.form
        return summarize(data["text"])


@app.route('/face/', methods=['GET', 'POST'])
def face_match():
    if request.method == 'POST':
        data = request.form
        source, target = data['source'], data['target']
        return face_eval(source, target)


@app.route('/patient/', methods=['GET', 'POST'])
def patient():
    if request.method == 'GET':
        pin = request.args.get('pin')
        dnh = DoctorNotesHelper()
        data = dnh.getNote(pin)
        res = {'message': data['notes'][-1]['message']}
        return jsonify(res)


@app.route('/sendNote/', methods=['POST'])
def sendNote():
    note = request.args['note']
    pin = request.args['pin']
    phoneNumber = request.args['phone']
    d = DoctorNotesHelper()
    d.addNoteForPatient(pin,note)
    sendText("Your doctor has sent you a new message based on your last phone call "
             " to Pillar: {}.".format(note),phoneNumber)
    sendText("Please go to your nearest Pillar Station to pick up your medications. "
             "Thank you.", phoneNumber)

    return ""

@app.route('/sPatient/<name>', methods=['GET'])
def getPatientDataFor(name):
    p = PatientDBHelper()
    return jsonify(p.getDataForPatientName(name))


@app.route('/patients/', methods=['GET'])
def patientData():
    p = PatientDBHelper()
    return jsonify(p.getAllPatients())


@app.route('/dispense/', methods=['POST'])
def dispensePing():
    pin = request.args.get('pin')
    pdb = PatientDBHelper()
    data = pdb.getDataForPatient(str(pin))
    dis = DispenseDBHelper()
    dis.toggleDispense()
    msg = "Your prescription is "
    for prescription in data['prescription']:
        msg += prescription['dosage'] + \
            ' of ' + prescription['name'] + \
            ' ' + prescription['instruction']
    msg += ' You will get a text for your next pickup!'
    res = {'num_prescriptions': len(data['prescription']), 'message': msg}
    return jsonify(res)

@app.route('/endcall',methods=['POST'])
def end():
    resp = VoiceResponse()
    resp.say("Thank you. Your information has been recorded and you should expect to hear "
             "back soon. In the mean time, we hope you feel better. Goodbye.")
    resp.hangup()
    return str(resp)


@app.route('/transcribe/<digits>',methods=['POST'])
def transcribe(digits):
    dbHelper = PatientDBHelper()
    dbHelper.addMedicalDataForPatient(digits,request.form['TranscriptionText'])
    return "Transcription added to Patient Database."

@app.route('/verification',methods=['POST'])
def verification():
    digits = request.form['Digits']
    patientDB = PatientDBHelper()
    resp = VoiceResponse()
    patient = patientDB.getDataForPatient(pin=digits,phone=request.form['Caller'])
    if(patient):
        resp.say("Welcome back to Pillar, {}. Please "
                 " describe your symptoms after the beep. When you are done,"
                 "please press the pound key. Thank you.".format(patient['name']))
        resp.record(finish_on_key="#", action="https://pillarrestapi.herokuapp.com/endcall"
                    ,method="POST",
                    transcribe_callback="https://pillarrestapi.herokuapp.com/transcribe/"
                                        + digits)
    else:
        resp.say("Sorry, we were unable to verify you. Goodbye.")

    return str(resp)
@app.route('/receivecall',methods=['POST'])
def receiveCall():
    resp = VoiceResponse()
    resp.say("Welcome to Pillar. "
             "Please enter your 4 digit verification code and press pound.")
    resp.gather(num_digits=4,action="https://pillarrestapi.herokuapp.com/verification")
    return str(resp)


@app.route('/sms/', methods=['POST'])
def sms():
    message = request.args.get('message')
    number = request.args.get('number')
    r = sendText(message, number)
    return "SMS Success"


@app.route('/call/', methods=['POST'])
def call():
    number = request.args.get('number')
    r = makeCall(number)
    return "Call Success"


if __name__ == "__main__":
    app.run(debug=False)
