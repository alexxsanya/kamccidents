from flask import Flask, render_template, jsonify, flash, redirect, url_for, request, Response,session
import json
import os
from . import init_app
from controllers.auth import Auth
app = init_app()
auth = Auth()
from models.user_model import UserSchema,UsersModel

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/feeds")
def feeds():

    return render_template("feeds.html")

@app.route("/dashboard")
@auth.login_required
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
    user = request.form.to_dict(flat=True)  

    user = UsersModel.get_user_by_login(user.get('user_name'))    
    print(">>> -> {} ".format(user))
    if '@' in str(user):
        session['username'] = str(user)

        flash('You were successfully logged in')

        return redirect(url_for('dashboard'))

    else: 

        error = {'error':"Login with wrong credentials"}

        return redirect(url_for('home',error=error))

@app.route("/logout",methods=['GET']) 
def logout():
    auth.logout()
    flash('You were successfully logged out')
    return redirect(url_for('home'))

@app.route("/create-user",methods=['POST'])
def create_user():
    req_data = request.form.to_dict(flat=True)

    req_data['firstname'],req_data['lastname'] =req_data.get('name').split(",") 

    print(">>> {} ".format(req_data))
    
    data, error = UserSchema().load(req_data)

    if error:
        return custom_response(error, 400)
  
  # check if user already exist in the db
    user_in_db = UsersModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}  
        return custom_response(message, 400)

    user = UsersModel(data)
    user.save()

    ser_data = UserSchema().dump(user).data

    return custom_response({'data': ser_data}, 201)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

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