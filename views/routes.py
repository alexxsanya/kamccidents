from flask_bootstrap import Bootstrap
from flask import Flask, render_template

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():

    return render_template("home.html")


