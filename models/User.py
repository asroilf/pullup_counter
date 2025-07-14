from peewee import * 

db = SqliteDatabase('new_db.db')

class User(Model):
    username = CharField(primary_key=True)
    name = CharField()

    class Meta:
        database = db

    def __str__(self):
        return self.name


