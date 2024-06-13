from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class QuoteForm(FlaskForm):
    text = StringField('Quote', validators=[DataRequired(), Length(max=500)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')