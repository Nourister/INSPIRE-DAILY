from flask import render_template, redirect, url_for, flash
from app import app, db
from app.models import Quote
from app.forms import QuoteForm
import random

quotes = [
    {"text": "The best way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
    {"text": "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.", "author": "Winston Churchill"},
    {"text": "Don’t let yesterday take up too much of today.", "author": "Will Rogers"},
    {"text": "You learn more from failure than from success. Don’t let it stop you. Failure builds character.", "author": "Unknown"},
    {"text": "It’s not whether you get knocked down, it’s whether you get up.", "author": "Vince Lombardi"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_quote', methods=['GET'])
def get_quote():
    # Fetch a random quote from the predefined list
    quote = random.choice(quotes)
    return render_template('quotes.html', quote=quote)

@app.route('/new_quote', methods=['GET', 'POST'])
def new_quote():
    form = QuoteForm()
    if form.validate_on_submit():
        existing_quote = Quote.query.filter_by(text=form.text.data, author=form.author.data).first()
        if existing_quote:
            flash('This quote already exists!', 'danger')
        else:
            new_quote = Quote(text=form.text.data, author=form.author.data)
            db.session.add(new_quote)
            db.session.commit()
            flash('Quote added successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('new_quote.html', form=form)

@app.route('/all_quotes', methods=['GET'])
def all_quotes():
    quotes_from_db = Quote.query.all()
    return render_template('all_quotes.html', quotes=quotes_from_db)