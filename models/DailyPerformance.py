from peewee import *
from models.User import User

db = SqliteDatabase('new_db.db')

class DailyPerformance(Model):
    user = ForeignKeyField(User, backref='past_records')
    reps = IntegerField()
    date = DateField()

    class Meta:
        database = db
        primary_key = CompositeKey('user', 'date')


