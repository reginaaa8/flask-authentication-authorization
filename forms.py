from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import Length 

class RegisterUserForm(FlaskForm):
    username = StringField("Username")

    password = PasswordField("Password")
    
    email = EmailField("Email")

    first_name = StringField("First Name", 
                             validators=[Length(min=1, max=30)])

    last_name = StringField("Last Name", 
                             validators=[Length(min=1, max=30)])

class UserLoginForm(FlaskForm):
    username = StringField("Username")

    password = PasswordField("Password")

class FeedbackForm(FlaskForm):
    title = StringField("title")
    
    content = StringField("content")
