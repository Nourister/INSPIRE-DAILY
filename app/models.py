from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.author}: {self.text}"
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # @property
    # def password(self):
    #     raise AttributeError('Password is not a readable attribute')
    
    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password=password)
    
    def verify_password(self, password):
        return self.password == password
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"
