from peewee import Model, AutoField, BlobField, ForeignKeyField
from .User import User
from .db import DB

class VideoHash(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref='videos')
    video_hash = BlobField()

    class Meta:
        database = DB

