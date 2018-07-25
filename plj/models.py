import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    # username = CharField(unique=True)
    # email = CharField(unique=True)
    password = CharField(unique=True)
    # is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        # order_by = ('-joined_at',)  # Should be tuple, hence comma.

    # def get_posts(self):
    #    return Post.select().where(Post.user == self)

    # def get_stream(self):
    #    return Post.select().where(
    #        (Post.user << self.following()) |
    #        (Post.user == self)
    #    )
    
    #def following(self):
    #    """The users that current_user is following."""
    #    return (
    #        User.select().join(
    #            Relationship, on=Relationship.to_user
    #        ).where(
    #            Relationship.from_user == self
    #        )
    #    )

    # def followers(self):
    #    """The users that are following current_user."""
    #    return (
    #        User.select().join(
    #            Relationship, on=Relationship.from_user
    #        ).where(
    #            Relationship.to_user == self
    #        )
    #    )

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
    title = CharField()
    learned = TextField()
    resources = TextField()
    minutes = IntegerField()

    class Meta:
        database = DATABASE
        order_by =  ('-datestamp',)  # Should be tuple, hence comma.

# class Relationship(Model):
#    # from_user = ForeignKeyField(User, related_name='relationships')
#    # to_user = ForeignKeyField(User, related_name='related_to')

#    class Meta:
#        database = DATABASE
#        indexes = (
#            (('from_user', 'to_user'), True)
#        )

def initialize():
    """Call the connect(), create_tables() and close() method on our db."""
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()
