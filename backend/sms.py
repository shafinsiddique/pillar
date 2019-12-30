from twilio.rest import Client
import json
from config import account_sid, auth_token
client = Client(account_sid, auth_token)
def sendText(message, number):
    return client.messages.create(
        body=message,
        from_='+12564877652',
        to=number
    )

if __name__ == "__main__":
    print(sendText("Hi, Shafin.", "+16478918425"))
