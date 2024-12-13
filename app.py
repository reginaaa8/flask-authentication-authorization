"""Auth Exercise"""
from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
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
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}

        new_user = User(**data)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/secret")
    
    else:
        return render_template("register_user.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def user_login():
    """user login"""
    form = UserLoginForm()

    if form.validate_on_submit():

        return redirect("/secret")

    return render_template("user_login.html", form=form)

@app.route("/secret")
def secret():
    """show logged in user secret page"""
    return render_template("secret.html")


