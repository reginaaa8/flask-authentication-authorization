"""Auth Exercise"""
from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, bcrypt, Feedback
from forms import RegisterUserForm, UserLoginForm, FeedbackForm


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

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """delete user"""
    if "username" not in session or username != session['username']:
        flash("You are not authorized to view this page. Please sign in", "danger") 
        return redirect("/login")
    
    user = User.query.get_or_404(username)
    # delete all the user's feedback
    Feedback.query.filter_by(username=username).delete()

    # delete the user from the db
    db.session.delete(user)
    db.session.commit()

    # remove user from session 
    session.pop("username")
    
    flash("Your account has been deleted", "danger")
    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def add_feedback(username):
    """show form for user to add feedback"""
    if "username" not in session or username != session['username']:
        flash("You are not authorized to view this page. Please sign in", "danger") 
        return redirect("/login")
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(title=form.title.data, content=form.content.data, username=username)
        
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("add_feedback.html", form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """allow user to edit previously posted feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("You are not authorized to view this page. Please sign in", "danger") 
        return redirect("/login")
    
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f'/users/{feedback.username}')

    form.title.data = feedback.title
    form.content.data = feedback.content
    
    return render_template("edit_feedback.html", form=form, feedback=feedback)
    





