from flask import Flask, render_template, jsonify, flash, redirect, url_for, request, Response,session
import json
import os
from . import init_app
from controllers.auth import Auth
from models.user_model import UserSchema,UsersModel
from models.accident_model import (AccidentsModelSchema, 
                                   AccidentsModel,
                                   AccidentStatModel,
                                   AccidentStatModelSchema)

from werkzeug import secure_filename

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
    
@app.route("/login",methods=['POST'])
def login_user():
    user = request.form.to_dict(flat=True)  

    user = UsersModel.get_user_by_email(user.get('user_name'))    
    
    user = UserSchema().dump(user).data 

    if user != None and '@' in str(user.get('email')):
        session['username'] = user.get('email')
        session['user_id'] = user.get('id')

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

@app.route("/create-accident", methods=['POST'])
#@auth.login_required
def create_accident():
    req_data = request.form.to_dict(flat=True)
    accident_photo = request.files['acc_photo']
    photo_name = accident_photo.filename
    req_data['acc_photo'] = photo_name
    req_data['acc_involved'] = str(request.form.getlist('acc_involved'))
    req_data['acc_is_victim'] = False
    if "acc_is_victim" in req_data:
        req_data['acc_is_victim'] = True
        
    #accident_photo.save(secure_filename(photo_name))
    #print(req_data)
    data1, error1 = AccidentsModelSchema().load(req_data)

    if error1:
        return custom_response(error1, 400)

  # check if this acccident is not already in the db
    accident_in_db = AccidentsModel.get_accident_by_title(req_data.get('acc_title'))
    if str(accident_in_db) != "None":
        message = 'Accident already exists in the database'
        flash(message,'error')        
        return redirect(url_for('home'))

    new_accident = AccidentsModel(data1)
    new_accident.save()
    new_accident_data = AccidentsModelSchema().dump(new_accident).data 
    
    #Adding accident statistics to the stat tab
    acc_id = new_accident_data.get('id')
    if type(acc_id) is int:
        req_data['acc_id'] = acc_id 
        data2, error2 = AccidentStatModelSchema().load(req_data)
        if error1:
            return custom_response(error, 400)
        new_accident_stat = AccidentStatModel(data2)
        new_accident_stat.save() 

        message = "Accident Added Successfully"
        flash(message,'success')        
        return redirect(url_for('home'))
    else:
        message = "Error 142 occured"
        flash(message,'error')        
        return redirect(url_for('home'))
        
@app.route("/all-accidents/<int:user_id>",methods=['GET'])
def get_user_accident_report(user_id):
    accident =  AccidentsModel.get_all_accidents(user_id) 
    data = AccidentsModelSchema().dump(accident, many=True).data
    print(data)
    return jsonify(data)

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