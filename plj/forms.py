from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField, IntegerField,
                     DateField)
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Length, EqualTo)


class LoginForm(Form):
    """Get password for full site functionality."""
    password = PasswordField("Password",
                             validators=[DataRequired()])


class PostForm(Form):
    """Validate journal entries."""
    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(message='Title should be less than 150 chars.', max=150)
        ])
    learned = TextAreaField(
        "What did you learn?",
        validators=[DataRequired()]
    )
    resources = TextAreaField(
        "Resources to remember?",
        validators=[DataRequired()]
    )
    minutes = IntegerField(
        "Minutes spent studying",
        validators=[DataRequired()]
    )
    datestamp = DateField(
        "Date: 1983-07-21",
        validators=[DataRequired()])
    tags = StringField(
        "Tags",
        validators=[
            Length(message='Tags must be less than 50 chars.', max=50)
        ])
