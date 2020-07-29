# This is where I initialise my application, and bring together its components.

# Necessary Imports
from flask import Flask

# Importing SQL Alchemy
from flask_sqlalchemy import SQLAlchemy

# Importing Flask Bcrypt for Hashing Passwords
from flask_bcrypt import Bcrypt

# Importing Login package
from flask_login import LoginManager

# Initialising the App
app = Flask(__name__)

# A secret key for encryption to protect against hacking
app.config['SECRET_KEY'] = 'b84fd909956dc9ecfc1f258078ebe953'

# References the location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# An instance of an SQLAlchemy database
db = SQLAlchemy(app)

# Initialising the Bcrypt module
bcrypt = Bcrypt(app)

# Initialising login manager
login_manager = LoginManager(app)

# Allows only accessing certain page when login session is active
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from quiz_program import routes