from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)

# load default settings file
app.config.from_object('scribble.default_settings')

# override settings with file pointed to by SCRIBBLE_CONFIG
app.config.from_envvar('SCRIBBLE_CONFIG', silent=True)

# noinspection PyUnresolvedReferences
import scribble.views
