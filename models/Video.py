from peewee import Model, AutoField, BlobField, ForeignKeyField
from .User import User
from service.db import DB

class Video(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref='videos')
    video_hash = BlobField()

    class Meta:
        database = DB

