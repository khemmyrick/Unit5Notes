import datetime

from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Regexp, ValidationError

# from models import User


class PostEntry(Form):
    user_name = StringField(
        'User Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z ]+$',
                message=("User should have first and last name, with space.")
            )])
    task_name = StringField(
        'Task Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_ ]+$',
                message=("Task name should be letters, numbers,"
                         "spaces, hyphens and underscores only.")
            )])
    timestamp = DateTimeField(default=datetime.datetime.now,
                              format='%Y-%m-%d %H:%M:%S')
    task_minutes = IntegerField(default=0)
    task_notes = TextAreaField('Notes?',
                               validators=[DataRequired()])
