import imghdr
import os
import smtplib
from email.message import EmailMessage
from typing import Final
from dotenv import load_dotenv


load_dotenv()
EMAIL_PASSWORD: Final[str] = os.getenv('EMAIL_PASSWORD')

PATH = os.path.join(os.path.dirname(__file__), "dementia-door-yellow.jpg")

email_subject = "Email test from Python"
sender_email_address = 'excellenteamembedded@gmail.com'
receiver_email_address = 'excellenteamembedded@gmail.com'
email_smtp = "smtp.gmail.com"


def send_email():
    """
    Send an e-mail with image
    """
    # create an email message object
    message = EmailMessage()
    # configure email headers
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address
    # set email body text
    message.set_content("Hello from Python!")
    with open(PATH, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    # set smtp server and port
    server = smtplib.SMTP(email_smtp, '587')
    # identify this client to the SMTP server
    server.ehlo()
    # secure the SMTP connection
    server.starttls()
    # login to email account
    server.login(sender_email_address, EMAIL_PASSWORD)
    # send email
    server.send_message(message)
    # close connection to server
    server.quit()


if __name__ == "__main()__":
    send_email()
