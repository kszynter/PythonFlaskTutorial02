from flask import Flask, render_template, flash

from content_management import content

TOPIC_DICT = content()

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("main.html")


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    return render_template("login.html")


@app.route('/dashboard/')
def dashboard():
    flash("flash test!!!")
    return render_template("dashboard.html", TOPIC_DICT=TOPIC_DICT)


@app.route('/slashboard/')
def slashboard():
    try:
        # intentionally buggy code sentence
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
