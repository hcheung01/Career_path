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
from models.apply import Apply
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
import uuid
import json
from hashlib import md5
from flask_mail import Message, Mail
from web_dynamic import app, login_manager


@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.route("/profile", methods=['GET'])
@login_required
def profile():
    return render_template("profile.html")

@app.route("/profile/new",  methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        profile = Profile(user_id = current_user.id,
                        position = form.position.data,
                        location = form.location.data
        )
        for skill_id in form.skill.data:
            skill = storage.get('Skill', skill_id)
            profile.skills.append(skill)
        # if form.more_skill.data:
        #     skill_list = form.more_skill.data.split(',')
        #     for skill in skill_list:
        #         new_skill = Skill(name=skill)
        #         storage.new(new_skill)
        #         profile.skills.append(new_skill)
        storage.new(profile)
        storage.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_profile.html',
                            title='Profile',
                            form=form,
                            method='POST')
