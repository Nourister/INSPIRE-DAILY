from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, bcrypt
from app.models import Quote, User
from app.forms import QuoteForm, LoginForm, RegistrationForm
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
@login_required
def get_quote():
    # Fetch a random quote from the predefined list
    quote = random.choice(quotes)
    return render_template('quotes.html', quote=quote)

@app.route('/new_quote', methods=['GET', 'POST'])
@login_required
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
@login_required
def all_quotes():
    quotes_from_db = Quote.query.all()
    return render_template('all_quotes.html', quotes=quotes_from_db)

@app.route('/search', methods=['GET'])
@login_required
def search_quotes():
    query = request.args.get('query')
    if query:
        search_results = Quote.query.filter(Quote.text.contains(query) | Quote.author.contains(query)).all()
    else:
        search_results = []
    return render_template('search_results.html', quotes=search_results, query=query)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check your email and password.', 'danger')
        else:
            flash('You have not registered yet. Please register first.', 'danger')
            return redirect(url_for('register'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))