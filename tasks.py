import base64
import json

from dotenv import load_dotenv
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

def gmail_send_message(user_data):
  
  name = user_data["username"]
  message = EmailMessage()

  message.set_content(f"Welcome!{name}. You have registered successfully!")

  message["To"] = user_data["email"]
  message["From"] = "tasnim.kuet.ece.1809003@gmail.com"
  message["Subject"] = "Register mail"

  # Encode the message as bytes and encode it to a URL-safe base64 string
  data={'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
  # Load credentials from token.json file
  with open('token.json', 'r') as token_file:
    credentials_data = token_file.read()

  credentials = Credentials.from_authorized_user_info(json.loads(credentials_data))
  # Build Gmail service with provided credentials
  service = build('gmail', 'v1', credentials=credentials)

  # Send email
  try:
    sent_message = service.users().messages().send(userId='me', body=data).execute()
    print('Message sent successfully!')
    return True
  except HttpError as e:
    print(f'An error occurred while sending the email: {e}')