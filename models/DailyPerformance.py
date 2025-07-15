from peewee import Model, IntegerField, DateField, CompositeKey, ForeignKeyField
from .User import User
from .db import DB

class DailyPerformance(Model):
    user = ForeignKeyField(User, backref='past_records')
    reps = IntegerField()
    date = DateField()

    class Meta:
        database = DB
        primary_key = CompositeKey('user', 'date')


