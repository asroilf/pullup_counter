from peewee import Model, CharField
from .db import DB

class User(Model):
    username = CharField(primary_key=True)
    name = CharField()

    class Meta:
        database = DB

    def __str__(self):
        return self.name


