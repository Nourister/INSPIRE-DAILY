from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nouristerjuma'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/juman/OneDrive/Desktop/INSPIRE DAILY/nourister.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('nourister juma', 'nouristerjuma@gmail.com')

from app import routes  # Import routes after initializing app and extensions
from app.models import User, Quote

# Create database tables if they do not exist
# Note: This approach is simple but not recommended for production.
# For production, use Flask-Migrate for better management of database schema changes.
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))