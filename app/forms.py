from app import app, db
from itsdangerous import TimedSerializer as Serializer
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from email_validator import validate_email, EmailNotValidError
from .models import User
from flask_wtf.file import FileField, FileRequired

class QuoteForm(FlaskForm):
    text = StringField('Quote', validators=[DataRequired(), Length(max=500)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), Length(min=6), EqualTo('password1')])
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        """Validate if the username exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise EmailNotValidError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        try:
            validate_email(email.data)
        except EmailNotValidError as e:
            raise ValueError('Invalid email address')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')