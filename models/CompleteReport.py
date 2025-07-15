from peewee import *
from .db import DB

class CompleteReport(Model):
    message_id=IntegerField(primary_key=True)
    message = TextField()

    class Meta:
        database = DB


