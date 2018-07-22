import datetime

from peewee import *


db = SqliteDatabase('log.db')


class Entry(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user_name = CharField(max_length=500)
    task_name = CharField(max_length=1000)
    task_minutes = IntegerField(default=0)
    task_notes = TextField()

    class Meta:
        database = db

def initialize():
    """Create database and table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)
