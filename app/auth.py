from flask import Blueprint, flash, redirect, render_template, url_for
from .forms import SignUpForm, LoginForm, ChangePasswordForm
from .models import Customer
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password2

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully. You can Login')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created. Email already exists')
            
            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''
        else:
            flash('Passwords do not match')
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                if current_user.id == 1:
                    return redirect('/admin-page')
                return redirect('/all_products')
            else:
                flash('Incorrect Password or Email')
        else:
            flash('Account does not exist. Signup first')
            return redirect('/sign-up')

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')


@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    customer = Customer.query.get(customer_id)
    return render_template('profile.html', customer=customer)

@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = ChangePasswordForm()
    customer = current_user
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Password has been changed successfully')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('Passwords do not match')
        else:
            flash('Password is incorrect')
    return render_template('change_password.html', form=form)