from app import db
from itsdangerous import TimedSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer)

    def __str__(self):
        return f"{self.author}: {self.text}"
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def verify_password(self, password):
        return self.password == password
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"