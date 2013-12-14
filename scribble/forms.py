from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Email, \
    Length, Regexp, ValidationError
from wtforms.fields.html5 import EmailField
from models import User


class Unique(object):
    def __init__(self, cls, key, message=None):
        self.cls = cls
        self.key = key
        if not message:
            message = u'{0} already exists in database.'.format(
                key.capitalize())
        self.message = message

    def __call__(self, form, field):
        if self.cls.has(self.key, field.data):
            raise ValidationError(self.message)


class RegisterForm(Form):
    invalid = 'Username must contain only letters, numbers, "_" and "-"'
    username = StringField('Username',
                           [InputRequired(), Length(min=4, max=63),
                            Regexp(r'^[A-Za-z0-9_-]+$', message=invalid),
                            Unique(User, 'username')])
    email = EmailField('Email Address', [InputRequired(), Email()])
    display_name = StringField('Display Name',
                               [InputRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', [InputRequired(),
                                          Length(min=8, max=255),
                     EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
