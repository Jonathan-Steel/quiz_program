# Necessary Imports
from flask import Flask, render_template, url_for, flash, redirect

# Importing the necessary forms
from forms import RegistrationForm, LoginForm

# Importing SQL Alchemy
from flask_sqlalchemy import SQLAlchemy

# Other imports
from datetime import datetime

# Initialising the App
app = Flask(__name__)

# A secret key for encryption to protect against hacking
app.config['SECRET_KEY'] = 'b84fd909956dc9ecfc1f258078ebe953'

# References the location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# An instance of an SQLAlchemy database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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
    form = RegistrationForm()

    # If the form is validated
    if form.validate_on_submit():

        # Sends a quick message. success is a Boostrap class.
        flash(f'Account created for {form.username.data}!', 'success')

        # Redirects us to the home page.
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # If the form is validated
    if form.validate_on_submit():

        # Temporary validation
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
            
    return render_template('login.html', title='Login', form=form)

# Running the App
if __name__ == '__main__':
    app.run(debug=True)