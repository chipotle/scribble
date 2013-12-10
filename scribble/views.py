from flask import render_template, request, redirect

from scribble import app
from models import *

@app.route('/')
def index():
    """A none-too-useful index page."""
    return render_template('index.html', name='Scribble')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if request.method == 'GET':
        return render_template('register.html')
    else:
        ok = User.create(request.form['username'],
                         request.form['password'])
        if ok:
            return redirect('/')
        return render_template('register.html', error=True)
