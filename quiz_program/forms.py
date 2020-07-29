# Importing the forms module from Flask.
from flask_wtf import FlaskForm

# Importing the String and Password and Submit and Boolean fields
from wtforms import StringField, PasswordField, SubmitField, BooleanField

# Importing validators
from wtforms.validators import DataRequired, Length, Email, EqualTo

# These Python Classes can automatically be converted into HTML forms

# Creating the registration form by inheriting properties from the default form.
class RegistrationForm(FlaskForm):
    # Creating a string field with a label of 'Username' where data is required and is a certain length.
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

# Creating the login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')