from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import random
from app import app, db, bcrypt, mail
from app.models import Quote, User
from app.forms import QuoteForm, LoginForm, RegistrationForm


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
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('This email address is already registered. Please use a different email or log in.', 'danger')
            return redirect(url_for('register'))  # Redirect back to the registration page
        else:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.password = form.password1.data
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')

            # Send a random quote to the new user's email
            quote = random.choice(quotes)
            msg = Message(subject='Welcome to Inspire Quotes!',
                          recipients=[form.email.data])
            msg.body = f'Hello {form.username.data},\n\nWelcome to Inspire Quotes! Here is your random quote:\n\n"{quote["text"]}" - {quote["author"]}'
            
            try:
                mail.send(msg)
                flash('A random quote has been sent to your email!', 'info')
            except Exception as e:
                flash('Failed to send the random quote to your email. Please contact support.', 'danger')
                app.logger.error(f"Failed to send email: {str(e)}")

            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Send email to nouristerjuma@gmail.com
        recipients = ['nouristerjuma@gmail.com']
        msg = Message(subject='New Contact Form Submission',
                      recipients=recipients)
        msg.body = f'You have received a new message from {name} ({email}):\n\n{message}'
        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            app.logger.error(f"Failed to send email: {str(e)}")

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/test_email')
def test_email():
    msg = Message(subject='Test Email',
                  recipients=['your-email@gmail.com'])
    msg.body = 'This is a test email.'
    try:
        mail.send(msg)
        return 'Test email sent!'
    except Exception as e:
        return f'Failed to send test email: {str(e)}'