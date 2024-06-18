from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from email_validator import validate_email, EmailNotValidError

class QuoteForm(FlaskForm):
    text = StringField('Quote', validators=[DataRequired(), Length(max=500)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        try:
            validate_email(email.data)
        except EmailNotValidError as e:
            raise ValueError('Invalid email address')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')