from flask import Flask, render_template, flash, request, url_for, redirect, session

from content_management import content
from dbconnect import connection
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
from wtforms import Form, BooleanField, TextField, PasswordField, validators

import gc

TOPIC_DICT = content()

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("main.html")


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Repeat Password')

    accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the '
                              '<a href="/privacy/">Privacy Notice</a> last updates June 2015...', [validators.Required()])


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            c, conn = connection()
            result = c.execute("SELECT * FROM users WHERE username = '%s'" % (thwart(username)))

            if int(result) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)
            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-tutorial")))
                conn.commit()

                flash("Thanks for registering!")

                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template('register.html', form=form)

    except Exception as e:
        return str(e)


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # todo, remove flashing details for a release
            # flash(attempted_username)
            # flash(attempted_password)

            # todo, replace it later with a database data comparison
            if attempted_username == "admin" and attempted_password == "admin":
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid credentials. Try again."

        return render_template("login.html", error=error)

    except Exception as e:
        flash(e)
        return render_template("login.html", error=error)

    return render_template("login.html")


@app.route('/dashboard/')
def dashboard():
    flash("flash test!!!")
    return render_template("dashboard.html", TOPIC_DICT=TOPIC_DICT)


@app.route('/slashboard/')
def slashboard():
    try:
        # todo, remove the buggy sentence for a release
        return render_template("dashboard.html", TOPIC_DICT=ssas)
    except Exception as e:
        return render_template("500.html", error=e)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
