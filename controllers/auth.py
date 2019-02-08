from functools import wraps
from flask import g, request, url_for, session, redirect,abort
from os import environ 

class Auth():
    def __init__(self):
        pass

    def login_required(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "username" in session:
                print(">>> {}".format(session))
            else:  
                abort(401)

            return f(*args, **kwargs)
        return decorated_function
    
    @staticmethod
    def logout():
        session.pop("username",None)
        return True