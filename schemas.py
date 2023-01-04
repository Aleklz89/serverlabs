from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    ID = fields.Int(dump_only=True)
    Username = fields.Str(required=True)


class CategorySchema(Schema):
    ID = fields.Int(dump_only=True)
    Name = fields.Str(required=True)


class RecordQuerySchema(Schema):
    User_ID = fields.Int(required=True, validate=validate.Range(min=1))
    Category_ID = fields.Int(validate=validate.Range(min=1))


class RecordSchema(Schema):
    ID = fields.Int(dump_only=True)
    User_ID = fields.Int(required=True, validate=validate.Range(min=1))
    Category_ID = fields.Int(required=True, validate=validate.Range(min=1))
    Amount = fields.Float(required=True, validate=validate.Range(min=0))