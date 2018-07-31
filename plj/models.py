import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    password = CharField(unique=True)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("User already exists")


class Post(Model):
    """Model class is a TextField and a DateTimeField.
    order_by is set to '-datestamp', reverse datestamp order.
    Meaning when Post.select() is called, the latest entry shows up first."""
    datestamp = DateField(default=datetime.datetime.today)
    title = CharField(max_length=150)
    learned = TextField()
    resources = TextField()
    minutes = IntegerField()

    class Meta:
        database = DATABASE
        order_by = ('-datestamp',)  # Should be tuple, hence comma.


def initialize():
    """Call the connect(), create_tables() and close() method on our db."""
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()
