from flask import render_template

from scribble import app

@app.route('/')
def index():
    """A none-too-useful index page."""
    return render_template('index.html')