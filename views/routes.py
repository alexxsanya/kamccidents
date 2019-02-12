from flask import Flask, render_template, jsonify, flash, redirect, url_for, request, Response,session
import json
import os
from . import init_app
from controllers.auth import Auth
from models.user_model import UserSchema,UsersModel
app = init_app()
auth = Auth()

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

    user = UsersModel.get_user_by_email(user.get('user_name'))    
    
    if '@' in str(user):
        session['username'] = str(user)

        flash('You are successfully logged in','success')

        return redirect(url_for('dashboard'))

    else: 

        flash('Logged in with wrong credentials','error')

        return redirect(url_for('home'))

@app.route("/logout",methods=['GET']) 
def logout():
    auth.logout()
    flash('You are successfully logged out','success')
    return redirect(url_for('home'))

@app.route("/create-user",methods=['POST'])
def create_user():
    req_data = request.form.to_dict(flat=True)

    req_data['firstname'],req_data['lastname'] =req_data.get('name').split(",")  
    
    data, error = UserSchema().load(req_data)

    if error:
        return custom_response(error, 400)
  
  # check if user already exist in the db
    user_in_db = UsersModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = 'User already exist with supplied email address'
        flash(message,'error')        
        return redirect(url_for('home'))

    user = UsersModel(data)
    user.save()

    #ser_data = UserSchema().dump(user).data
    message = "Account Created, Now Login"
    flash(message,'success')        
    return redirect(url_for('home'))

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
    error = {
        'title':"Error 401 Occured",
        'desc':"You are unathorized to access this resource",
        'tip':"Please first login to access this page.",
        'url':"/",
        'action':"Get Me Out of Here"
    }
    return render_template("error.html",**locals())

@app.errorhandler(403)
def error_403(error):
    error = {
        'title':"Error 403 Occured",
        'desc':"You are forbidden from accessing this resource",
        'tip':"Contact Admin for details on why.",
        'url':"/contact",
        'action':'Contact Support Team'
    }
    return render_template("error.html",**locals())

@app.errorhandler(404)
def error_404(error):    
    error = {
        'title':"Error 404 Occured!",
        'desc':"Requested Resource Not Found",
        'tip':"The resource you are trying to access does not exist here",
        'url':"/",
        'action':"Get Me Out of Here"
    }
    return render_template("error.html",**locals())

@app.errorhandler(405)
def error_405(error):
    error = {
        'title':"Error 405 Occured!",
        'desc':"Method Not Allowed",
        'tip':"The method is not allowed for the requested URL.",
        'url':"/",
        'action':"Get Me Out of Here"
    }
    return render_template("error.html",**locals())

@app.errorhandler(500)
def error_500(error):
    error = {
        'title':"Server Error 500 Occured",
        'desc':"An Internal Error Occured",
        'tip':"Contact system support unit for assistance on this Erro",
        'url':"/contact",
        "action":"Contact Support Team"
    }
    return render_template("error.html",**locals())