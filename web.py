from flask import Flask, url_for, request, render_template, redirect, session, flash
from passlib.hash import sha256_crypt #encrypting the password

import forms

users_db = {'demo':sha256_crypt.encrypt('demo')}

app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Index and other pages
@app.route('/')
def index():
    return render_template("index.html")

# Signup
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup/donor_signup', methods=['GET', 'POST'])
def donor_signup():
    form = forms.UserSignupForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        users_db[username] = password
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('donor_signup.html', form=form)

@app.route('/signup/organization_signup', methods=['GET', 'POST'])
def organization_signup():
    form = forms.OrganizationSignupForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        users_db[username] = password
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('donor_signup.html', form=form)


# Authentication
@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    del session['logged_in_user']
    return redirect('/')

@app.route('/login_form', methods=['POST'])
def login_form():
    username = request.form['username']
    password = request.form['password']
    if username in users_db and sha256_crypt.verify(password, users_db[username]):
        session['logged_in_user'] = username
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error="Wrong credentials!")

if __name__ == '__main__':
    app.secret_key = 'not-so-secret-key'
    app.run(debug=True)


