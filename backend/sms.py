from twilio.rest import Client
import json
account_sid = "AC05c393f8d847379407a03bd90a4a21a5"
auth_token = "05b0b84317e5452b9e87f95d453a1729"
client = Client(account_sid, auth_token)
def sendText(message, number):
    return client.messages.create(
        body=message,
        from_='+12564877652',
        to=number
    )

if __name__ == "__main__":
    print(sendText("Hi, Shafin.", "+16478918425"))
