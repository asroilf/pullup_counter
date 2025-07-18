from peewee import *
from service.db import DB

class Report(Model):
    message_id=IntegerField(primary_key=True)
    message = TextField()

    class Meta:
        database = DB


