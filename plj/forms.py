from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, IntegerField,
                     DateField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)

# from models import User


# def name_exists(form, field):
#    if User.select().where(User.username == field.data).exists():
#        raise ValidationError('User with that name already exists.')


# def email_exists(form, field):
#    if User.select().where(User.email == field.data).exists():
#        raise ValidationError('User with that email already exists.')


# class RegisterForm(Form):
#    username = StringField(
#        'Username',
#        validators=[
#            DataRequired(),
#            Regexp(
#                r'^[a-zA-Z0-9_]+$',
#                message=("Username should be one word, letters, "
#                         "numbers, and underscores only.")
#            ),
#            name_exists
#        ])
#    email = StringField(
#        'Email',
#        validators=[
#            DataRequired(),
#            Email(),
#            email_exists
#        ])
#    password = PasswordField(
#        'Password',
#        validators=[
#            DataRequired(),
#            Length(min=2),
#            EqualTo('password2', message='Passwords must match')
#        ])
#    password2 = PasswordField(
#        'Confirm Password',
#        validators=[DataRequired()]
#    )
    

class LoginForm(Form):
    """Get password for full site functionality."""
    # email = StringField('Email',
    #                    validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])


class PostForm(Form):
    """Only form called.
    Populates form with prompt for user.
    Checks for data while accepting submission."""
    title = StringField("Title",
                        validators=[DataRequired()])
    learned = TextAreaField("What did you learn?",
                            validators=[DataRequired()])
    resources = TextAreaField("Resources to remember?",
                              validators=[DataRequired()])
    minutes = IntegerField("Minutes spent studying",
                           validators=[DataRequired()])
    datestamp = DateField("Date: 1983-07-21",
                          # format='%Y-%m-%d',
                          validators=[DataRequired()])
