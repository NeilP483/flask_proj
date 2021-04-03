from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username   = StringField('Username', validators=[DataRequired()])
    email      = StringField('Email', validators=[DataRequired(), Email()])
    password   = PasswordField('Password', validators=[DataRequired()])
    password2  = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit     = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.get_with_username(username.data)
        if user is not None:
            raise ValidationError('Username already exists. Use another one.')
    def validate_email(self, email):
        user = User.get_with_email(email.data)
        if user is not None:
            raise ValidationError('Please use another email.')

class NewLog(FlaskForm):
    choices = []
    choices.append('Running')
    choices.append('Walking')
    choices.append('Swimming')
    choices.append('Jogging')
    choices.append('Yoga')
    choices.append('Other')
    print(choices)
    activity_type = SelectField("Activity Type:", choices=[(c, c) for c in choices])
    time = FloatField("Time of execise (in mins):")
    heart_rate = IntegerField("What was your heart rate?:")
    submit = SubmitField("Add New Log")
