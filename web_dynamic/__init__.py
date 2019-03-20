from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Message, Mail
from models import storage

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'teamcareer.up'
app.config['MAIL_PASSWORD'] = 'Dreamteam@hbtn'
app.url_map.strict_slashes = False


@login_manager.user_loader
def load_user(user_id):
    all_users = storage.all('User').values()
    for user in all_users:
        if user.id == user_id:
            return user

from web_dynamic import acc_mngt
from web_dynamic import profile_mngt
