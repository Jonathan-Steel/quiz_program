# File to contain all of the routes.

# Necessary Imports
from flask import render_template, url_for, flash, redirect, request

# Importing the initialised app
from quiz_program import app, db, bcrypt

# Importing the database models (tables)
from quiz_program.models import User, Question, Quiz, Chapter, Textbook

# Importing the necessary forms
from quiz_program.forms import RegistrationForm, LoginForm, UpdateAccountForm

# Importing useful stuff from the login package
from flask_login import login_user, current_user, logout_user, login_required

# Secrets module for creating random hex digits
import secrets

# OS module
import os

# Image adjustment module
from PIL import Image

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
        return redirect(url_for('quizzes'))

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
            return redirect(next_page) if next_page else redirect(url_for('quizzes'))

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

# Saving the users picture to file system
def save_picture(form_picture):

    # Random Hex for filename
    random_hex = secrets.token_hex(8)

    # Splits filename from its extension and discards the filename
    _, f_ext = os.path.splitext(form_picture.filename)

    # Creates filename and extension
    picture_fn = random_hex + f_ext

    # Creates the path to the image
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Adjusts the size of the image to 125x125 to save space
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Saves the picture to the filesystem
    i.save(picture_path)

    return picture_fn

# Account Page (Decorator means that user needs to be logged in to access route)
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        # If the user has changed their profile picture
        if form.picture.data:

            # Get the picture filename
            picture_file = save_picture(form.picture.data)

            # Update the database
            current_user.image_file = picture_file

        # Updating information in the SQL database when submitting form information.
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash('Your account has been updated!', 'success')

        return redirect(url_for('account'))

    elif request.method == 'GET':

        # Populates the form with current users data when loading the page.

        form.username.data = current_user.username
        form.email.data = current_user.email

    # References the user's image file stored in the static directory.
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)

# Quizzes Page
@app.route("/quizzes")
@login_required
def quizzes():
    quizzes = Quiz.query.all()
    quiz_lengths = []
    for quiz in quizzes:
        quiz_lengths.append(len(list(quiz.questions)))
    return render_template('quizzes.html', title='Quizzes', quizzes=quizzes, quiz_lengths=quiz_lengths)

# Quizzes Page
@app.route("/quiz/<int:quiz_id>")
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id)
    return render_template('quiz.html', title=quiz.title, quiz=quiz, questions=questions)