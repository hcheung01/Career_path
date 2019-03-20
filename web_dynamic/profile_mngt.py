#!/usr/bin/python3
"""
Flask App that integrates with CareerUp static HTML Template
"""
from flask import render_template, url_for, flash, redirect, request, Flask, jsonify, abort
from models import storage
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import requests
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, ProfileForm
# from .forms import PostForm, ReviewForm
from models.user import User
from models.profile import Profile
from models.job import Job
from models.skill import Skill
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
    all_profile = storage.all('Profile').values()
    profile_list = []
    for prof in all_profile:
        if prof.user_id == current_user.id:
            profile_list.append(prof)
    all_jobs = storage.all('Job').values()
    job_list = []
    for job in all_jobs:
        if job.user_id == current_user.id:
            job_list.append(job)
    return render_template("profile.html",
                            profile_list=profile_list,
                            job_list=job_list)

@app.route("/profile/new",  methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    skills = ["python", "javascript", "html", "css", "ruby", "bash",
                   "linux", "unix", "rest", "restful", "api", "aws",
                   "cloud", "svn", "git", "junit", "testng", "java", "php",
                   "agile", "scrum", "nosql", "mysql", "postgresdb", "postgres",
                   "shell", "scripting", "mongodb", "puppet", "chef", "ansible",
                   "nagios", "sumo", "nginx", "haproxy", "docker", "automation",
                   "jvm", "scikit-learn", "tensorflow", "vue", "react", "angular",
                   "webpack", "drupal", "gulp", "es6", "jquery", "sass", "scss",
                   "less", "nodejs", "node.js", "graphql", "postgresql", "db2",
                   "sql", "spring", "microservices", "kubernates", "swagger",
                   "hadoop", "ci/cd", "django", "elasticsearch", "redis", "c++",
                   "c", "hive", "spark", "apache", "mesos", "gcp", "jenkins",
                   "azure", "allcloud", "amqp", "gcp", "objective-c", "kotlin"
                   "kafka", "jira", "cassandra", "containers", "oop", "redis",
                   "memcached", "redux", "bigquery", "bigtable", "hbase", "ec2",
                   "s3", "gradle", ".net", "riak", "shell", "hudson", "maven",
                   "j2ee", "oracle", "swarm", "sysbase", "dynamodb", "neo4",
                   "allcloud", "grunt", "gulp", "apex", "rails", "mongo", "apis",
                   "html5", "css3", "rails", "scala", "rasa", "soa", "soap",
                   "microservices", "storm", "flink", "gitlab", "ajax",
                   "micro-services", "oop", "saas", "struts", "jsp", "freemarker",
                   "hibernate", "rlak", "solidity", "heroku", "ecs", "gce",
                   "scripting", "perl", "c#", "golang", "xml", "newrelic",
                   "grafana", "helm", "polymer", "closure", "backbone",
                   "atlassian", "angularjs", "flask", "scikitlearn", "theano",
                   "numpy", "scipy", "panda", "tableau", "gensim", "rpc",
                   "graphql", "iaas", "paas", "azure", "es", "solr", "http", "iot",
                   "kinesis", "lambda", "typescript", "gradle", "buck", "bazel"]
    if form.is_submitted() and form.errors == {}:
        print("check herer 2")
        profile = Profile(user_id = current_user.id,
                        position = form.position.data,
                        location = form.location.data,
                        skills = form.more_skill.data
        )
        storage.new(profile)
        storage.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('profile'))
    return render_template('create_profile.html',
                            title='Profile',
                            form=form,
                            skills=skills,
                            method='POST')

@app.route('/profile_delete/<profile_id>')
@login_required
def profile_delete(profile_id=None):
    """
        profile route to handle http methods for given place
    """
    profile_obj = storage.get('Profile', profile_id)
    if profile_obj is None:
        flash('Your profile does not exist!', 'danger')
    profile_obj.delete()
    del profile_obj
    flash('Your profile has been deleted!', 'success')
    return redirect(url_for('profile'))

@app.route('/profile_update/<profile_id>', methods=['GET', 'POST'])
@login_required
def profile_update(profile_id=None):
    """
        profile route to handle http methods for given place
    """
    profile_obj = storage.get('Profile', profile_id)
    if profile_obj is None:
        flash('Your profile does not exist!', 'danger')
    form = ProfileForm()
    if form.is_submitted() and form.errors == {}:
        profile_obj.position = form.position.data
        profile_obj.location = form.location.data
        profile_obj.skills = form.more_skill.data
        profile_obj.save()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    else:
        form.position.data = profile_obj.position
        form.location.data = profile_obj.location
    return render_template('create_profile.html',
                            title='Profile',
                            form=form,
                            method='POST')

@app.route('/job_update/<job_id>', methods=['GET', 'PUT'])
@login_required
def job_update(job_id=None):
    job_obj = storage.get('Job', job_id)
    if job_obj is None:
        abort(404)
    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if 'applied' in req_json.keys():
            if req_json['applied'] == '':
                del req_json['applied']
        if 'interview' in req_json.keys():
            if req_json['interview'] == '':
                del req_json['interview']
        print(req_json)
        job_obj.bm_update(req_json)
    return render_template('profile.html')

@app.route('/job_delete/<job_id>', methods=['GET', 'PUT'])
@login_required
def job_delete(job_id=None):
    job_obj = storage.get('Job', job_id)
    if job_obj is None:
        abort(404)
    job_obj.delete()
    return render_template('profile.html')


@app.route('/job_search_profile/<profile_id>', methods=['GET'])
@login_required
def job_search_profile(profile_id):
    jobs = requests.get('http://0.0.0.0:5001/api/v1/job_search_by_profile/' + profile_id)
    return render_template('job_search_profile.html',
                            jobs=jobs.json(),
                            user_id=current_user.id)

@app.route('/job_add/<user_id>/<job_db_id>', methods=['GET', 'POST'])
@login_required
def job_add(user_id=None, job_db_id=None):
    job_db_obj = storage.get('Job_db', job_db_id)
    if job_db_obj is None:
        abort(404, 'Not found')
    new_job = Job(
        company = job_db_obj.company,
        position = job_db_obj.position,
        location = job_db_obj.location,
        description = job_db_obj.description,
        user_id = user_id
    )
    storage.new(new_job)
    storage.save()
    return render_template('job_detail.html', job_db_obj=job_db_obj)
