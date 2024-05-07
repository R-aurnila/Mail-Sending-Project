import json
import base64

from flask import jsonify 
from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from db import db
from models import UserModel
from schemas import UserPostSchema
from schemas import UserRegisterSchema
from tasks import gmail_send_message


blp = Blueprint("Users", "users", description="Operations on users")



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
        current_app.queue.enqueue(gmail_send_message, user_data)
        


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










