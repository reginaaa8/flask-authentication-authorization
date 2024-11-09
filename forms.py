from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import Length 

class RegisterUserForm(FlaskForm):
    username = StringField("Pet Name")

    password = StringField("Password")
    
    email = EmailField("Email")

    first_name = StringField("First Name", 
                             validators=[Length(min=1, max=30)])

    last_name = StringField("Last Name", 
                             validators=[Length(min=1, max=30)])