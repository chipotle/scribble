from flask import render_template, redirect

from scribble import app
from models import *
from forms import RegisterForm

@app.route('/')
def index():
    """A none-too-useful index page."""
    return render_template('index.html', name='Scribble')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User({
            'username': form.username.data,
            'password': form.password.data,
            'email': form.email.data,
            'display_name': form.display_name.data
        })
        user.save()
        return redirect('/')
    return render_template('register.html', form=form)
