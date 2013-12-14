from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Email, Length, Regexp


class RegisterForm(Form):
    invalid = 'Username must contain only letters, numbers, "_" and "-"'
    username = StringField('Username',
                           [InputRequired(), Length(min=4, max=63),
                            Regexp(r'[A-Za-z0-9_-',
                                   message=invalid)])
    email = StringField('Email Address', [InputRequired(), Email()])
    display_name = StringField('Display Name',
                               [InputRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', [InputRequired(),
                     EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
