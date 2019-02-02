from flask_bootstrap import Bootstrap
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/feeds")
def feeds():

    return render_template("feeds.html")

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")

@app.route("/personal-report")
def personal_report():
    personal_report = [{
        "id": 1,
        "title": "Item 1",
        "location":"Ntinda"
    },{
        "id": 2,
        "title": "Item 2",
        "location":"Kampala"
    }]
    return json.dumps(personal_report)

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