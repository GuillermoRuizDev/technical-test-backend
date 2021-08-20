# models.py

# pip

import peewee as pw

# app
from app.db import db

class BaseModel(pw.Model):
    """Base model class. All descendants share the same database."""
    def __marshallable__(self):
        return dict(self.__dict__)['_data']

    class Meta:
        database = db


class User(BaseModel):
    email = pw.CharField(max_length=100, unique=True)
    password = pw.CharField()
    first_name = pw.CharField()
    last_name = pw.CharField()
    created_at = pw.DateTimeField()
    updated_at = pw.DateTimeField()

class Nota(BaseModel):
    content = pw.TextField()
    title = pw.CharField()
    is_done = pw.BooleanField(default=False)
    user = pw.ForeignKeyField(User)
    posted_on = pw.DateTimeField()

    class Meta:
        order_by = ("-posted_on",)

def create_tables():
    db.connect()
    User.create_table(True)
    Nota.create_table(True)
