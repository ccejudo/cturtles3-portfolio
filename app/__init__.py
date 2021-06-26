from flask import Flask, Response, render_template, url_for, request, redirect, json, flash
from flask_toastr import Toastr
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
import json

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db.init_app(app)
toastr = Toastr(app)

data_file = open('./app/static/data.json')
data = json.load(data_file)
#data_file.close()

########## Back ##########

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db_instance = db.get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db_instance.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db_instance.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db_instance.commit()
            flash(f"User {username} created successfully", 'success')
        else:
            flash(error, 'error')

    ## TODO: Return a register page
    return render_template("register.html")

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db_instance = db.get_db()
        error = None
        user = db_instance.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            flash("Login Successful", 'success')
        else:
            flash(error, 'error')
    
    ## TODO: Return a login page
    return render_template("login.html")

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
    return Response( status=200 )

if __name__ == "__main__":
    app.run() 
