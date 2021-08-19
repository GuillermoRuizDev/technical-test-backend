from re import I
from marshmallow import (Schema, fields, post_dump, post_load, pre_load,
                         validate)
from werkzeug.security import check_password_hash, generate_password_hash
import datetime as dt

from app.models import Nota

class UserSchema(Schema):
    # class Meta:
    #     ordered = True

    id = fields.Int(dump_only=True)
    name = fields.String(dump_only=True)
    email = fields.String(
        required=True,
        validate=validate.Email(error="Not a valid email address"),
    )
    password = fields.Method(
        required=True,
        deserialize="hashed_password",
        validate=[validate.Length(min=6, max=36)],
        load_only=True
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def hashed_password(self, value):
        return generate_password_hash(value)

    # Clean up data
    @pre_load
    def process_input(self, data, **kwargs):
        data["email"] = data["email"].lower().strip()
        return data

    # We add a post_dump hook to add an envelope to responses
    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "users" if many else "user"
        return {key: data}

class NotaSchema(Schema):
    id = fields.Int(dump_only=True)
    done = fields.Boolean(attribute="is_done", missing=False)
    user = fields.Nested(UserSchema(exclude=("joined_on", "password")), dump_only=True)
    content = fields.Str(required=True)
    posted_on = fields.DateTime(dump_only=True)

    # Again, add an envelope to responses
    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        key = "notas" if many else "nota"
        return {key: data}

    # We use make_object to create a new Todo from validated data
    @post_load
    def make_object(self, data, **kwargs):
        if not data:
            return None
        return Nota(
            content=data["content"],
            title=data["title"],
            is_done=data["is_done"],
            posted_on=dt.datetime.utcnow(),
        )

user_schema = UserSchema()
nota_schema = NotaSchema()
notas_schema = NotaSchema(many=True)