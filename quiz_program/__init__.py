# This is where I initialise my application, and bring together its components.

# Necessary Imports
from flask import Flask

# Importing SQL Alchemy
from flask_sqlalchemy import SQLAlchemy

# Initialising the App
app = Flask(__name__)

# A secret key for encryption to protect against hacking
app.config['SECRET_KEY'] = 'b84fd909956dc9ecfc1f258078ebe953'

# References the location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# An instance of an SQLAlchemy database
db = SQLAlchemy(app)

from quiz_program import routes