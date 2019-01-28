from flask_bootstrap import Bootstrap
from flask import Flask, render_template

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():

    return render_template("home.html")


@app.errorhandler(401)
def error_401(error):
    return render_template("401.html")

@app.errorhandler(403)
def error_401(error):
    return render_template("403.html")

@app.errorhandler(404)
def error_401(error):
    return render_template("404.html")

@app.errorhandler(500)
def error_401(error):
    return render_template("500.html")