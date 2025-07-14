from peewee import *

db = SqliteDatabase('new_db.db')

class CompleteReport(Model):
    message_id=IntegerField(primary_key=True)
    message = TextField()

    class Meta:
        database = db


