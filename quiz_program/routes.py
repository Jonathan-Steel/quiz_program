# File to contain all of the routes.

# Necessary Imports
from flask import render_template, url_for, flash, redirect, request

# Importing the initialised app
from quiz_program import app, db, bcrypt

# Importing the database models (tables)
from quiz_program.models import User, Post

# Importing the necessary forms
from quiz_program.forms import RegistrationForm, LoginForm

# Importing useful stuff from the login package
from flask_login import login_user, current_user, logout_user, login_required

# Creating the Home Page
# The following links redirect the user to the home.html file
@app.route("/")
@app.route("/home")
def home():
    # Returns HTML template
    return render_template('home.html')

# About Page
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# Register Page
# Allows GET and POST requests
@app.route("/register", methods=['GET', 'POST'])
def register():

    # If user is already logged in return them to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    # If the form is validated
    if form.validate_on_submit():

        # Makes hashed version of password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Creating an instance of the user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        # Adding user to the database
        db.session.add(user)
        db.session.commit()

        # Sends a quick message. success is a Boostrap class.
        flash(f'Your account has been created! You are now able to login!', 'success')

        # Redirects us to the login page.
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():

    # If user is already logged in return them to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    # If the form is validated
    if form.validate_on_submit():

        # Checks that email exists in the database.
        user = User.query.filter_by(email=form.email.data).first()

        # Checks whether user exists and checks that hashed passwords match.
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # Logs the user in (creates a session) and allows remember me option.
            login_user(user, remember=form.remember.data)

            # If there is a next page the user wants access (maybe an account page) after logging in, this will collect it.
            next_page = request.args.get('next')

            # Ternary return for next page system.
            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
            
    return render_template('login.html', title='Login', form=form)

# Logout Route
@app.route("/logout")
def logout():

    # Simply ends the session, logging the user out.
    logout_user()

    # Returns them to the home page
    return redirect(url_for('home'))

# Account Page (Decorator means that user needs to be logged in to access route)
@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
