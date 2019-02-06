from flask import Flask, render_template, jsonify, flash, redirect, url_for, request
import json
import os
from . import init_app

app = init_app()

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
        "title": "Accident 1",
        "location":"Ntinda"
    },{
        "id": 2,
        "title": "Accident 2",
        "location":"Kampala"
    }]
    return json.dumps(personal_report)

@app.route("/login",methods=['POST'])
def login_user():
    flash('You were successfully logged in')
    return redirect(url_for('dashboard'))

@app.errorhandler(401)
def error_401(error):
    return render_template("401.html")

@app.errorhandler(403)
def error_403(error):
    return render_template("403.html")

@app.errorhandler(404)
def error_404(error):
    return render_template("404.html")

@app.errorhandler(405)
def error_405(error):
    return render_template("405.html")

@app.errorhandler(500)
def error_500(error):
    return render_template("500.html")