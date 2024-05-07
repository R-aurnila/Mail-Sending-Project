import json
from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import base64
from email.message import EmailMessage

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from db import db
from sqlalchemy import or_
from models import UserModel
from schemas import UserPostSchema
from schemas import UserRegisterSchema


blp = Blueprint("Users", "users", description="Operations on users")


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


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
          UserModel.email == user_data["email"],
        ).first():
            abort(409, message="A user with that email already exists.")
        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],

        )
        
        db.session.add(user)
        db.session.commit()
        gmail_send_message(user_data)


        return {"message": "User created successfully."}, 201
    
    
user_blp = Blueprint('user', 'user', url_prefix='/user')     
@blp.route("/user")
class User(MethodView):
    @blp.arguments(UserPostSchema, location='json')
    def post(self, email):
        if isinstance(email, dict):
            email = email.get('email', '')
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # Add other attributes as needed
        }
        
        return jsonify(user_data), 200










