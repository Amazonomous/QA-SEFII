from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import SignUpForm
import re

from .extensions import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect login details, please try again', category='error')
        else:
            flash('User does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST':
        email = form.email.data
        username = form.username.data
        password = form.password.data
        password_confirmation = form.password_confirmation.data

        if not "@" in email:
            flash('Please enter a valid email address with an @ symbol', category='error')
        if not len(username) >= 4:
            flash('Please enter a username with 4 or more characters', category='error')
        if not re.match(r'^[a-zA-Z]+$', username):
            flash('Please enter a valid username with only alphabet letters', category='error')
        elif password != password_confirmation:
            flash('Passwords do not match', category='error')
        else:
            existingEmails = User.query.filter_by(email=email).first()
            existingUsers = User.query.filter_by(username=username).first()

            if existingEmails or existingUsers:
                flash('Cannot register as this account exists', category='error')
                return render_template('sign_up.html', form=form, user=current_user)
            
            new_user = User(email=email, username=username, password=generate_password_hash(
                    password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True) # We want the user to login again rather than sign them in immediately
            flash('Account created', category='success')
            return redirect(url_for('auth.login'))
    
    return render_template('sign_up.html', form=form, user=current_user)