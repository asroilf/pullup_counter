from peewee import * 

db = SqliteDatabase('new_db.db')

class User(Model):
    username = CharField(primary_key=True)
    name = CharField()

    class Meta:
        database = db

    def __str__(self):
        return self.name

class DailyPerformance(Model):
    user = ForeignKeyField(User, backref='past_records')
    reps = IntegerField()
    date = DateField()

    class Meta:
        database = db
        primary_key = CompositeKey('user', 'date')

class CompleteReport(Model):
    message_id=IntegerField(primary_key=True)
    message = TextField()

    class Meta:
        database = db

class VideoHash(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref='videos')
    video_hash = BlobField()

    class Meta:
        database = db
