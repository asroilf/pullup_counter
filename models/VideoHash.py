from peewee import *
from models.User import User
db = SqliteDatabase('new_db.db')

class VideoHash(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref='videos')
    video_hash = BlobField()

    class Meta:
        database = db

