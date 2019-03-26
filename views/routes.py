from flask import (Flask, 
                    render_template, 
                    jsonify, flash, 
                    redirect, url_for, request, 
                    Response,session,abort,
                    send_from_directory)
import json
import os
from datetime import datetime
from . import init_app
from controllers.auth import Auth
from controllers.util import Util
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
    stat =  AccidentStatModel.get_all_stat() 
    stats = AccidentStatModelSchema().dump(stat, many=True).data 

    accident =  AccidentsModel.get_accidents_from_db() 
    acc_data = AccidentsModelSchema().dump(accident, many=True).data 
    
    minor = len([a for a in stats if ((a['acc_no_dead'] <1 or\
                     a['acc_no_major'] < 4) and\
                         a['acc_no_minor']>0)])
    major = len([a for a in stats if (a['acc_no_dead'] < 5 and\
                    a['acc_no_major'] >5)])
    fatal = len([a for a in stats if (a['acc_no_dead'] > 5)])

    boda_involved = len([a for a in acc_data if 'Boda' in a['acc_involved']])

    taxis_involved = len([a for a in acc_data if 'Taxi' in a['acc_involved']])

    dead_count = 0
    for acc in stats:
        dead_count += acc['acc_no_dead']
    
    return render_template("dashboard.html", **locals())

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

    req_data['firstname'],req_data['lastname'] =req_data.get('name').split(" ")  
    
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
@auth.login_required
def create_accident():
    req_data = request.form.to_dict(flat=True)
    accident_photo = request.files['acc_photo']
    photo_name = accident_photo.filename
    req_data['acc_photo'] = photo_name
    req_data['acc_involved'] = str(request.form.getlist('acc_involved'))
    req_data['acc_is_victim'] = False
    if "acc_is_victim" in req_data:
        req_data['acc_is_victim'] = True
    photo_name = secure_filename(photo_name)
    
    if Util.allowed_photos(photo_name):
        path = "views/"+os.path.join(app.config['UPLOAD_FOLDER'],photo_name)
        accident_photo.save(path)

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
@auth.login_required
def get_user_accident_report(user_id):
    accident =  AccidentsModel.get_all_accidents(user_id) 
    data = AccidentsModelSchema().dump(accident, many=True).data 
    return jsonify(data)

@app.route("/all-accidents")
def get_all_accidents():
    all_accident =  AccidentsModel.get_accidents_from_db() 
    data = AccidentsModelSchema().dump(all_accident, many=True).data 
    return jsonify(data)
    
@app.route("/accident/<int:accident_id>")
@auth.login_required
def get_accident(accident_id): 
    accident = AccidentsModel.get_one_accident(accident_id)    
    accident_stat = AccidentStatModel.get_accident_stat(accident_id)
    
    if not accident or not accident_stat:
        abort(413) # Using 413 in place of 204 No Content Found

    accident = AccidentsModelSchema().dump(accident).data

    stat = AccidentStatModelSchema().dump(accident_stat).data 

    data = {**accident,**stat}

    return render_template("accident.html",accident=data)
    #return custom_response(data, 200)

@app.route("/delete/accident/<int:accident_id>", methods=['POST'])
@auth.login_required
def delete_accident(accident_id):
    accident = AccidentsModel.get_one_accident(accident_id)
    if not accident:
        abort(404)
    data = AccidentsModelSchema().dump(accident).data
    accident.delete()
    flash('Accident {}, deleted'.format(data.get('acc_title')),'success')
    return redirect(url_for('dashboard'))

@app.route('/uploaded_files/<img_uri>')
def get_photo(img_uri): 
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img_uri)


@app.route('/reports/charts')
def generate_chart_report():
    acc_involved = ['Bodas','Taxis','Pedestrians','Lorry','Buses']
    accident =  AccidentsModel.get_accidents_from_db() 
    data = AccidentsModelSchema().dump(accident, many=True).data 
    list = []
    for x in acc_involved:
        item = [a for a in data if x in str(a)]
        new_item = [x.title(),len(item)]
        list.append(new_item)

    per_area = []
    kampala_areas = []
    for ac in data:
        kampala_areas.append(ac['acc_area_name'])

    for area in kampala_areas:
        count = len([a for a in data if area == a['acc_area_name']])
        per_area.append([area, count])

    per_hour = []
    know_hours = []
    for ac in data:
        acc_time = datetime.fromisoformat(ac['acc_time'])
        know_hours.append(acc_time.strftime('%H'))

    for hour in set(know_hours):
        count = len([a for a in data\
            if hour == datetime.fromisoformat(a['acc_time']).strftime('%H')]\
            )
        per_hour.append([hour,count])
    per_hour.sort()
    return render_template('chart_report.html',**locals())

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

@app.errorhandler(413)
def no_content_found(error):
    error = {
        'title':"No Data Found",
        'desc':"No Accident Data is found in the system for the specified URI",
        'tip':"Wong Accident Object.",
        'url':"/dashboard",
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