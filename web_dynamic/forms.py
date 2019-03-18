from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import FormField
from models import storage
from flask import flash
from flask_login import current_user



class RegistrationForm(FlaskForm):
    first_name = StringField('first_name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('last_name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    phone = StringField('phone')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_email(self, email):
        all_users = storage.all('User').values()
        for user in all_users:
            if user.email == email.data:
                raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# class ReviewForm(FlaskForm):
#     text = StringField('text',
#                            validators=[DataRequired(), Length(min=1, max=100)])
#     submit = SubmitField('Submit')



class UpdateAccountForm(FlaskForm):
    first_name = StringField('first_name',
                           validators=[Length(min=2, max=20)])
    last_name = StringField('last_name',
                            validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone_number')
    submit = SubmitField('Update')
    def validate_email(self, email):
        all_users = storage.all('User').values()
        for user in all_users:
            if user.email == email.data and user.email != current_user.email:
                raise ValidationError('That email is taken. Please choose a different one.')


class ProfileForm(FlaskForm):
    position = StringField('position', validators=[DataRequired(), Length(min=2, max=20)])
    location = StringField('location')
    all_skills = storage.all('Skill').values()
    skills = SelectMultipleField('skills',
                                    choices = [(skill.id, skill.name) for skill in all_skills],
                                    widget=widgets.ListWidget(prefix_label=True),
                                    option_widget=widgets.CheckboxInput())
    more_skill = StringField('more_skill')
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        all_users = storage.all('User').values()
        if email.data not in [user.email for user in all_users]:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
