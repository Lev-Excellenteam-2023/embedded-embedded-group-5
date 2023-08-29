from typing import Final
from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()
TWILIO_ACCOUNT_SID: Final[str] = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN: Final[str] = os.getenv('TWILIO_AUTH_TOKEN')
FROM_NUMBER: Final[str] = os.getenv('FROM_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class NotificationManager:
    def __int__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def notify_user(self, to_number, message_to_send):
        message = self.client.messages \
            .create(
                 body=message_to_send,
                 from_=FROM_NUMBER,
                 to=to_number
             )

        print(message.sid)
