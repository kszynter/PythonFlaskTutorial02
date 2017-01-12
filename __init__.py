from flask import Flask, render_template, flash, request, url_for, redirect

from content_management import content

TOPIC_DICT = content()

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("main.html")


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

    # app.debug = True
    app.run()
