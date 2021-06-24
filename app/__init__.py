from flask import Flask, render_template, url_for, request, redirect, json
from . import db
import os
import json

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app)

data_file = open('./app/static/data.json')
data = json.load(data_file)
#data_file.close()

########## Back ##########


########## Front ##########

#Create URL routes
@app.route('/')
def home():
    allUsers = data
    return render_template("home.html", allUsers=allUsers)

#Create URL for each members
@app.route('/about/<string:name>')
def about(name):
    userData = data[name]
    allUsers = data
    return render_template("about.html", name=name, userData=userData, allUsers=allUsers)

@app.route('/health')
def health():
    if request.method == 'GET':
        return flask.Response( status=200 )

if __name__ == "__main__":
    app.run() 
