import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
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
    """A class for individual journal entries."""
    datestamp = DateField(default=datetime.datetime.today)
    title = CharField()
    learned = TextField()
    resources = TextField()
    minutes = IntegerField()
    slug = CharField(unique=True)

    class Meta:
        database = DATABASE
        order_by = ('-datestamp', 'title')

    def get_tags(self):
        return Tag.select().where(Tag.called_by == self)

    def get_tag_stream(self):
        return Tag.select().where(
            (Tag.called_by == self)
        )

    def all_tags(self):
        """Tags called by this post."""
        return(
            Tag.select().join(
                TagTrend, on=TagTrend.post_call
            ).where(
                TagTrend.tag_by == self
            )
        )


class Tag(Model):
    term = CharField(unique=True,
                     max_length=50)
    slug = CharField(unique=True)
    first_use = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('term', 'first_use')

    def all_posts(self):
        """The entries that call this tag."""
        return (
            Post.select().join(
                TagTrend, on=TagTrend.tag_by
            ).where(
                TagTrend.post_call == self
            )
        )


class TagTrend(Model):
    post_call = ForeignKeyField(Tag,
                                related_name='chosen')
    tag_by = ForeignKeyField(Post,
                             related_name='caller')

    class Meta:
        database = DATABASE
        indexes = (
            (('post_call', 'tag_by'), True)
        )


def initialize():
    """Call the connect(), create_tables() and close() method on our db."""
    DATABASE.connection()
    DATABASE.create_tables([User, Post, Tag, TagTrend], safe=True)
    DATABASE.close()
