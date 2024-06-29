from app import db
from flask import render_template, redirect, url_for, flash, request, send_file, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from app.models import User
from app.populate_db import Quote
from sqlalchemy import func
import random
import io
from app import app, db, bcrypt, mail
from app.forms import QuoteForm, LoginForm, RegistrationForm, ResetPasswordForm, RatingForm



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_quote', methods=['GET'])
@login_required
def get_quote():
    try:
        quote = Quote.query.order_by(func.random()).first()

        if quote:
            app.logger.info(f"Quote fetched: {quote}")
            return render_template('quotes.html', quote=quote, form=RatingForm())
        else:
            app.logger.warning('No quotes found in the database.')
            flash('No quotes found in the database.', 'warning')
            return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Error fetching quote: {str(e)}")
        flash('Error fetching quote. Please try again later.', 'danger')
        return redirect(url_for('index'))


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
            return redirect(url_for('get_quote'))  # Redirect to get_quote after adding a new quote
    return render_template('new_quote.html', form=form)


@app.route('/all_quotes', methods=['GET'])
@login_required
def all_quotes():
    quotes_from_db = Quote.query.all()
    if not quotes_from_db:
        flash('No quotes found in the database.', 'info')
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
            return redirect(url_for('register'))  # Redirect back to the registration page or handle the error condition
        else:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.password = form.password1.data
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            # Optionally, perform additional actions after successful registration
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
            app.logger.info('Email sent successfully!')
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            app.logger.error(f"Failed to send email: {str(e)}")
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            app.logger.error(f"Failed to send email: {str(e)}")

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/test_email')
def test_email():
    msg = Message(subject='Test Email',
                  recipients=['nouristerjuma@gmail.com'])
    msg.body = 'This is a test email.'
    try:
        mail.send(msg)
        return 'Test email sent!'
    except Exception as e:
        return f'Failed to send test email: {str(e)}'


from flask import send_file, request, jsonify

@app.route('/download_quote', methods=['GET'])
@login_required
def download_quote():
    quote_text = request.args.get('quote_text')
    quote_author = request.args.get('quote_author')

    if not quote_text or not quote_author:
        return jsonify({'error': 'Quote text and author must be provided.'}), 400

    # Prepare the content of the quote as a text file
    content = f"{quote_text}\n- {quote_author}"

    # Create an in-memory buffer for the file content
    buffer = io.BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)  # Move the cursor to the beginning of the buffer

    # Return the file as a response using Flask's send_file function
    return send_file(
        buffer,
        as_attachment=True,  # Ensure the browser treats it as an attachment
        download_name="quote.txt",  # Specify the filename for the downloaded file
        mimetype='text/plain'  # Specify the MIME type of the file
    )

@app.route('/rate_quote/<int:quote_id>', methods=['POST'])
@login_required
def rate_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    form = RatingForm()

    if form.validate_on_submit():
        quote.rating = form.rating.data
        db.session.commit()
        flash('Thank you for your rating!', 'success')
    else:
        flash('Invalid rating. Please select a value between 1 and 5.', 'danger')

    return redirect(url_for('get_quote'))