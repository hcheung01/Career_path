from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import FormField
from models import storage
from flask import flash
from flask_login import current_user



class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone')
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



class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Phone Number')
    submit = SubmitField('Update')
    def validate_email(self, email):
        all_users = storage.all('User').values()
        for user in all_users:
            if user.email == email.data and user.email != current_user.email:
                raise ValidationError('That email is taken. Please choose a different one.')


class ProfileForm(FlaskForm):
    position = StringField('Position', validators=[DataRequired(), Length(min=2, max=20)])
    location = StringField('Location')
    more_skill = StringField('Add more skills')
    submit = SubmitField('Submit')

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
