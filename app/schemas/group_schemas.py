from marshmallow import Schema, fields, validate

class CreateGroupSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100),
        error_messages={"required": "Group name is required"}
    )
    description = fields.Str(required=False)


class UpdateGroupSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=False, validate=validate.Length(min=3, max=100))
    description = fields.Str(required=False)
