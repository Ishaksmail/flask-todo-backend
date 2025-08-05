from marshmallow import Schema, fields, validate

class RegistrationSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        error_messages={"required": "Username is required"}
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "Valid email is required"}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        error_messages={"required": "Password is required"}
    )


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
