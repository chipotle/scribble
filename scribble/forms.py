from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Email


class RegisterForm(Form):
    username = StringField('Username', [InputRequired()])
    email = StringField('Email Address', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired(),
                     EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
