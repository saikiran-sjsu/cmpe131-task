from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
    username = StringField('User Name')
    password = PasswordField('Password')
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    question = PasswordField('Secret Question', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TaskForm(FlaskForm):
    task_name = StringField('Task Name')
    description = StringField('Description')
    submit = SubmitField('Submit')
    yes = SubmitField('Yes')


class ForgotForm(FlaskForm):
    username = StringField('User Name')
    question = PasswordField('Secret Question')
    reset_password = PasswordField('Password')
    reset = SubmitField('Reset')
