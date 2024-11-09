from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import Length 

class RegisterUser(FlaskForm):
    username = StringField("Pet Name")

    password = StringField("Password")
    
    email = EmailField("Email")

    first_name = StringField("First Name", 
                             validators=Length(max=30))

    last_name = StringField("Last Name", 
                             validators=Length(max=30))