"""Auth Exercise"""
from flask import Flask, redirect, render_template, session, flash
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

        return redirect(f"/users/{new_user.username}")
    
    else:
        return render_template("register_user.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def user_login():
    """user login"""
    form = UserLoginForm()

    if form.validate_on_submit():

        user = User.authenticate(form.username.data, form.password.data)
        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    return render_template("user_login.html", form=form)

@app.route("/users/<username>")
def show_user_info(username):
    """show logged in user their info"""
    if "username" not in session or username != session['username']:
        flash("You are not authorized to view this page. Please sign in", "danger") 
        return redirect("/login")
    user = User.query.get_or_404(username)

    return render_template("user_info.html", user=user)
    
@app.route("/logout")
def logout():
    """log user our"""
    session.clear()
    return redirect("/")


