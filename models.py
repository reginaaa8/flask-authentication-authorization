"""Models for users and feedback"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """user"""
    __tablename__ = "users"
    
    username = db.Column(db.String(20), 
                     nullable=False, 
                     primary_key=True)
    
    password = db.Column(db.String, 
                     nullable=False)
    
    email = db.Column(db.String,
                          nullable=False)

    first_name = db.Column(db.String(30), 
                     nullable=False)
    
    last_name = db.Column(db.String(30), 
                     nullable=False)
    
    feedback = db.relationship("Feedback", backref="user")
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """register user with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else: 
            return False
        
class Feedback(db.Model):
    __tablename__ = "feedback"
    
    id = db.Column(db.Integer, 
                   autoincrement=True,
                   primary_key=True)
    
    title = db.Column(db.String(100), 
                     nullable=False)
    
    content = db.Column(db.String,
                          nullable=False)

    username = db.Column(db.String(20), 
                     db.ForeignKey('users.username'), 
                     nullable=False)
