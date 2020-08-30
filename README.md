## Links
° Youtube Demo Part 1: https://www.youtube.com/watch?v=ZaiWNKMNuig </br>
° Youtube Demo Part 2: https://www.youtube.com/watch?v=Fxb96g8-exg

## Description

° In rural villages, there are 2 main barriers to healthcare access. The first is the fact that there only a few doctors available for the entire village and the second is the fact that the nearest doctors and pharmacies are situated miles away.

° Pillar was built to tackle these issues.

° Pillar is a low-cost health care system in which instead of having to spend limited resources to visit the doctor, patients can simply describe their symptoms via a phone call. The transcription of the phone call gets sent to the doctor's portal. The doctor can then review the patients symptoms and leave notes for the patient as well as prescribe medications.

° The notes from the doctor is sent to the patient via an SMS and the patients can visit a Pillar station to pick up any medications that the doctor prescribed.

## How we built it

° The phone calls and SMS's are programmed using the Twilio Programmable Voice/SMS API. Once our Twilio number receives an incoming call, a request for instructions is sent to our own REST API. All information about the phone calls that Twilio sends to our server is stored in a MongoDB Atlas database.

° Our REST API was built using Python's Flask Framework and is currently deployed on Heroku. The server has a series of endpoints that the rest of our program can communicate with.

° The hardware component for this project, which is the actual Pillar Station was built using an Arduino and programmed in the C programming language. We used the Amazon Echo to allow patients to control our Pillar Stations via Voice. 


## List of Technologies Used

° [Twilio](https://www.twilio.com/)</br>
° [Flask](https://github.com/pallets/flask)</br>
° [Voiceflow](https://www.voiceflow.com/)</br>
° [AWS](https://aws.amazon.com/)</br>
° [Arduino](https://www.arduino.cc/)</br>
° [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)</br>






