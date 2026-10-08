import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(subject, content):
    params = {
        "from": os.getenv("EMAIL_FROM"),
        "to": [os.getenv("EMAIL_TO")],
        "subject": subject,
        "html": content,
    }

    response = resend.Emails.send(params)

    print("Email sent successfully!")
    print(response)