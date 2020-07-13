# Necessary Imports
from flask import Flask, render_template, url_for

# Initialising the App
app = Flask(__name__)

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

# Running the App
if __name__ == '__main__':
    app.run(debug=True)