from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)    

class UserPostSchema(Schema):
    email = fields.Email(required=True)
