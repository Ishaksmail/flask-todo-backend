from marshmallow import Schema, fields, validate

class CreateTaskSchema(Schema):
    text = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={"required": "Task text is required"}
    )
    due_at = fields.DateTime(required=False)
    group_id = fields.Int(required=False)


class UpdateTaskSchema(Schema):
    id = fields.Int(required=True)
    text = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    is_completed = fields.Boolean(required=False)
    due_at = fields.DateTime(required=False)


class TaskStatusSchema(Schema):
    id = fields.Int(required=True)
