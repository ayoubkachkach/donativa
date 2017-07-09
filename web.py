from flask import Flask, url_for, request, render_template, redirect, session, flash
from passlib.hash import sha256_crypt #encrypting the password
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

import helpers
import forms
import mysql_connector

from functools import wraps


users_db = {'demo':sha256_crypt.encrypt('demo')}
mylist = [1, 1, 1, 1, 1, 1]
app = Flask(__name__)
with app.test_request_context():
    app.config['UPLOAD_FOLDER_ACCOUNTS'] = "static/accounts/"
    app.config['UPLOAD_FOLDER_DONATIONS'] = "static/donations/"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = '3306'
app.config['MYSQL_DB'] = 'DONATIVA'
mysql = MySQL(app)
# mysql.init_app(app)

@app.route('/donation_page')
def donation_page():
    return render_template('donation_page.html')

def login_required(func):
    @wraps(func)
    def _wrapped_func(*args, **kwargs):
        if 'logged_in_user' not in session:
            return redirect(url_for('login'))
        else:
            return func(*args, **kwargs)
    return _wrapped_func

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
    triplets= helpers.group_list(mylist, 3)
    args = 1 #session['account_id']
    n_requests = mysql_connector.get_number_requests(mysql,args)
    myrequests = mysql_connector.get_requests(mysql,args)
    return render_template("index.html", triplets=triplets, myrequests=myrequests, n_requests=n_requests[0][0] )




# Signup
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup/donor_signup', methods=['GET', 'POST'])
def donor_signup():
    form = forms.UserSignupForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        city = form.city.data
        bio = form.bio.data
        address = form.address.data
        phone_number = form.phone_number.data
        email = form.email.data
        args = (email, username, password, bio, 1, first_name, last_name, address, city, phone_number)
        if mysql_connector.create_donor(mysql, args) == True:
            return redirect(url_for('login'))
        else:
            return render_template('donor_signup.html', error="Username or email already exists!",form=form)
    return render_template('donor_signup.html', form=form)

@app.route('/signup/organization_signup', methods=['GET', 'POST'])
def organization_signup():
    form = forms.OrganizationSignupForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        bio = form.bio.data
        address = form.address.data
        city = form.city.data
        phone_number = form.phone_number.data
        certification_code = form.certification_code.data
        args = (email, username, password, bio, 2, name, address, city, phone_number, certification_code)
        if mysql_connector.create_organization(mysql, args) == True:
            return redirect(url_for('login'))
        else:
            return render_template('organization_signup.html', form=form, error="Username or email already exists!")
        
    return render_template('organization_signup.html',form=form)

@app.route('/donation_add', methods=['GET', 'POST'])
def donation_add():
    form = forms.CreateDonationForm(request.form)
    form.donation_type.choices = mysql_connector.get_types(mysql)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data
        city = form.city.data
        address = form.address.data
        donation_type = form.donation_type.data
        donation_date = form.donation_date.data
        file = request.files['file']
        if file.filename == '':
            filename = 'none.jpg'
        if file and helpers.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            args = (title, description, city, donation_type, donation_date, address, filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_DONATIONS'], filename)
            helpers.ensure_dir(file_path)
            file.save(file_path)
        mysql_connector.add_donation(mysql, args)
        return redirect(url_for('login'))
    args = 1 #session account_id
    myrequests = mysql_connector.get_requests(mysql,args)
    n_requests = mysql_connector.get_number_requests(mysql,args)
    return render_template('donation_add.html', form=form,myrequests=myrequests ,n_requests=n_requests[0][0])
        


# Authentication
@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")
    
@app.route('/logout')
@login_required
def logout():
    del session['logged_in_user']
    return redirect('/')

@app.route('/login_form', methods=['POST'])
def login_form():
    username = request.form['username']
    password_candidate = request.form['password']
    args = (username, password_candidate)
    result = mysql_connector.login_user(mysql, args)
    if result[0] == True:
        session['logged_in'] = True
        session['logged_in_user'] = username
        session['type'] = result[1]
        session['account_id'] = result[2]
        return(redirect(url_for('index', username=username)))
    return render_template('login.html', error="Wrong credentials!")

#Profile
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    triplets= helpers.group_list(mylist, 2)
    args = 1 #session account_id
    myrequests = mysql_connector.get_requests(mysql,args) 
    n_requests = mysql_connector.get_number_requests(mysql,args)
    return render_template("profile.html", triplets=triplets, myrequests=myrequests, n_requests=n_requests[0][0])

#TO BE MODIFIED
@app.route('/donations_history/<username>', methods=['GET','POST'])
def donationshistory(username):
    args = 1 #session[account_id]
    myrequests = mysql_connector.get_requests(mysql,args)
    n_requests = mysql_connector.get_number_requests(mysql,args)
    return render_template("donationshistory.html", myrequests=myrequests, n_requests=n_requests[0][0])

if __name__ == '__main__':
    app.secret_key = 'not-so-secret-key'
    app.run(debug=True)


