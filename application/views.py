
from flask import render_template, request, Flask, session, redirect, url_for, escape

from application import app

app.secret_key = b'\xf9\x0bn\xe2[M\x80\xdf\xcdVV\x04\x04\x8e\xf5\xc0'

@app.route('/')
def index():
#    if 'username' in session:
#        return 'Logged in as %s' % escape(session['username'])
    return render_template("/saunat/saunat.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
