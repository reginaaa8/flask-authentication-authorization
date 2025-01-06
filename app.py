"""Auth Exercise"""
from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, bcrypt
from forms import RegisterUserForm, UserLoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///auth_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)

@app.route("/")
def index():
    """redirect to register"""
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """register new user"""
    form = RegisterUserForm()
    if form.validate_on_submit():
        new_user = User.register(
            form.username.data, 
            form.password.data, 
            form.email.data, 
            form.first_name.data, 
            form.last_name.data)

        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username

        return redirect("/secret")
    
    else:
        return render_template("register_user.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def user_login():
    """user login"""
    form = UserLoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        session["username"] = User.username

        return redirect("/secret")

    return render_template("user_login.html", form=form)

@app.route("/secret")
def secret():
    """show logged in user secret page"""
    if "username" in session:
        return render_template("secret.html")
    else:
        return redirect("/login")


