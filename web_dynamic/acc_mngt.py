#!/usr/bin/python3
"""
Flask App that integrates with CareerUp static HTML Template
"""
from flask import render_template, url_for, flash, redirect, request, Flask, jsonify
from models import storage
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import requests
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, ProfileForm
# from .forms import PostForm, ReviewForm
from models.user import User
from models.profile import Profile
from models.job import Job
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
import uuid
import json
from hashlib import md5
from flask_mail import Message, Mail
from web_dynamic import app, login_manager
mail = Mail(app)

@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.route('/')
@app.route('/home')
def home():
    """
    handles request to custom template
    """
    if current_user.is_authenticated:
        flash('you are loged in')
    jobs = requests.get('http://0.0.0.0:5001/api/v1/job_search_gereral')
    return render_template('home.html',
                           title='home', jobs=jobs.json())

@app.route('/job_search/<position>/<location>', methods=['GET', 'POST'])
def job_search(position=None, location=None):
    jobs = requests.get('http://0.0.0.0:5001/api/v1/job_search_by_criteria/' + position + '/' + location)
    if current_user.is_authenticated:
        return render_template('job_search.html',
                               title='job_search',
                               jobs=jobs.json(),
                               user_id=current_user.id)
    else:
        return render_template('job_search.html',
                               title='job_search',
                               jobs=jobs.json(),
                               user_id=None)

@app.route('/about')
def about():
    """
    handles request to custom template
    """
    if current_user.is_authenticated:
        flash('You are loged in.')
    return render_template('about.html', title='about')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """return login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        all_users = storage.all('User').values()
        for user in all_users:
            if user.email == form.email.data:
                pw = md5()
                pw.update(form.password.data.encode("utf-8"))
                if pw.hexdigest() == user.password:
                    user.authenticated = True
                    login_user(user, remember=form.remember.data)
                    next_page = request.args.get('next')
                    flash('Hello {} {}!'.format(user.first_name, user.last_name))
                    return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',
                            title='Login',
                            form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """return login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=form.password.data,
                        phone=form.phone.data)
        storage.new(new_user)
        storage.save()
        flash('Account created for {}!'.format(form.first_name.data), 'home')
        return redirect(url_for('login'))
    return render_template('register.html',
                            title='Register',
                            form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/update_account", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        storage.save()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    return render_template('update_account.html',
                        title='Account',
                        form=form,
                        user_id=current_user.id)

def send_reset_email(user):
    s = Serializer(app.config['SECRET_KEY'], 1800)
    token = s.dumps({'user_id': user.id}).decode('utf-8')
    msg = Message('Password Reset Request',
                    sender='teamcareer.up@gmail.com',
                    recipients=[user.email])
    msg.body = """To reset your password, visit the following link:
{}

If you did not make this request then simply ignore this email and no changes will be made.
""".format(url_for('reset_token', token=token, _external=True))
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        for user in storage.all('User').values():
            if user.email == form.email.data:
                send_reset_email(user)
                flash('An email has been sent with instructions to reset your password.', 'info')
                return redirect(url_for('login'))
    return render_template('reset_request.html',
                            title='Reset Password',
                            form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    user = storage.get('User', user_id)
    form = ResetPasswordForm()
    if form.validate_on_submit():
        pw = md5()
        pw.update(form.password.data.encode("utf-8"))
        user.password = pw.hexdigest()
        user.save()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',
                            title='Reset Password',
                            form=form)
