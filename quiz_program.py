# Necessary Imports
from flask import Flask, render_template, url_for, flash, redirect

# Importing the necessary forms
from forms import RegistrationForm, LoginForm

# Initialising the App
app = Flask(__name__)

# A secret key for encryption to protect against hacking
app.config['SECRET_KEY'] = 'b84fd909956dc9ecfc1f258078ebe953'

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