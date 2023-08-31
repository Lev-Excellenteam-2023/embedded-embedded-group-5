from typing import Final
from dotenv import load_dotenv
from twilio.rest import Client
import numpy as np
import os
from io import BytesIO
from PIL import Image
import smtplib
from email.message import EmailMessage

load_dotenv()
TWILIO_ACCOUNT_SID: Final[str] = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN: Final[str] = os.getenv('TWILIO_AUTH_TOKEN')
FROM_NUMBER: Final[str] = os.getenv('FROM_NUMBER')
EMAIL_PASSWORD: Final[str] = os.getenv('EMAIL_PASSWORD')
EMAIL_ADDRESS: Final[str] = os.getenv('EMAIL_ADDRESS')


class NotificationManager:
    """
    This class is responsible for sending notifications.
    """

    client: Client
    to_number: str
    to_email: str
    service: str

    def __init__(self, number: str, email: str, service_type: str):

        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.to_number = number
        self.to_email = email
        self.service = service_type

    def notify_user(self, message_to_send: str, frame) -> None:

        match self.service:
            case 'sms':
                self.send_sms(message_to_send)
            case 'email':
                self.send_email(message_to_send, frame)
            case 'all':
                self.send_sms(message_to_send)
                self.send_email(message_to_send, frame)
            case _:
                raise ValueError('not match found')

    def send_sms(self, message_to_send: str) -> None:

        message = self.client.messages.create(
            body=message_to_send,
            from_=FROM_NUMBER,
            to=self.to_number
        )

    def send_email(self, message_to_send: str, image_array: np.ndarray):
        message = EmailMessage()
        message['Subject'] = 'DOOR STATUS UPDATE'
        message['From'] = EMAIL_ADDRESS
        message['To'] = self.to_email
        message.set_content(message_to_send)

        image_pil = Image.fromarray(image_array)
        with BytesIO() as image_buffer:
            image_pil.save(image_buffer, format='JPEG')
            image_data = image_buffer.getvalue()

        image_name = "door_status.jpg"
        message.add_attachment(image_data, maintype='image', subtype='jpeg', filename=image_name)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)
        server.quit()

    def ask_doors(self, doors) -> None:
        # TODO
        pass
