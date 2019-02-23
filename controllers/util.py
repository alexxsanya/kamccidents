from flask import Flask
import config
app = Flask(__name__)
class Util():

    @staticmethod
    def allowed_photos(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.Config.ALLOWED_EXTENSIONS