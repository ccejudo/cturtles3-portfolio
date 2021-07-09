import os
import json
from flask import (
    Flask,
    Response,
    render_template,
    url_for,
    request,
    redirect,
    json,
    flash,
)
from flask_toastr import Toastr
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from . import db


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
toastr = Toastr(app)

data_file = open("./app/static/data.json")
data = json.load(data_file)


class UserModel(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash(f"User {username} created successfully", "success")
        else:
            flash(error, "error")

    ## TODO: Return a register page
    return render_template("register.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            flash("Login Successful", "success")
        else:
            flash(error, "error")

    ## TODO: Return a login page
    return render_template("login.html")


########## Front ##########

# Create URL routes
@app.route("/")
def home():
    allUsers = data
    return render_template("home.html", allUsers=allUsers)


# Create URL for each members
@app.route("/about/<string:name>")
def about(name):
    userData = data[name]
    allUsers = data
    return render_template(
        "about.html", name=name, userData=userData, allUsers=allUsers
    )


""" @app.route("/health")
def health():
    return "Works" """


if __name__ == "__main__":
    app.run()
