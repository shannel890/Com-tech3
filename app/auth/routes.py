from flask import Blueprint, render_template, redirect, url_for, flash
from app.form import RegistrationForm, LoginForm
from app.models.user import User
from app.extension import db
from flask_login import login_user, logout_user
import logging

auth = Blueprint('auth',__name__,url_prefix='/auth')


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already registered. Please use a different email.', 'danger')
                return render_template('auth/register.html', form=form)
            
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                password=form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f'Exception during registration: {e}', exc_info=True)
            flash('An error occurred during registration. Please try again later.', 'danger')
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        logging.info(f"Attempting login for user: {form.email.data}")
        if user:
            logging.info(f"User found: {user.email}")
            if user.verify_password(form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login successful!', 'success')
                logging.info("Login successful.")
                return redirect(url_for('dashboard.index'))
            else:
                logging.warning("Password verification failed.")
        else:
            logging.warning("User not found.")
        flash('Login failed. Please check your email and password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.landing_page'))