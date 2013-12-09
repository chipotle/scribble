from flask import Flask

app = Flask(__name__)

# load default settings file
app.config.from_object('scribble.default_settings')

# override settings with file pointed to by SCRIBBLE_CONFIG
app.config.from_envvar('SCRIBBLE_CONFIG', silent=True)

# noinspection PyUnresolvedReferences
import scribble.views
