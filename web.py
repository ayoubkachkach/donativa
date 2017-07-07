from flask import Flask, url_for, request, render_template, redirect, session, flash
from passlib.hash import sha256_crypt #encrypting the password
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

import helpers
import forms
import mysql_connector

from functools import wraps


users_db = {'demo':sha256_crypt.encrypt('demo')}
mylist = [1, 1, 1, 1, 1, 1]
app = Flask(__name__)
with app.test_request_context():
    app.config['UPLOAD_FOLDER'] = url_for('static', filename="/uploads/")

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
    return render_template("index.html", triplets=triplets)




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
    toadd = mysql_connector.get_types(mysql)
    form.donation_type.choices = mysql_connector.get_types(mysql)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data
        donation_type = form.donation_type.data
        city = form.city.data
        donation_date = form.donation_date.data.strftime('%x')
        file = request.files['file']
        if file.filename == '':
            upload_error='No selected file'
            return redirect(request.url, upload_error=upload_error)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("YEAAASOIFHASFHAOKHOKH "(title,description,donation_type,city,donation_date, filename))
            return render_template('login.html')
    return render_template('donation_add.html', form=form)
        


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
        return(redirect(url_for('index', username=username)))
    return render_template('login.html', error="Wrong credentials!")

#Profile
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    triplets= helpers.group_list(mylist, 2)
    return render_template("profile.html", triplets=triplets)

#TO BE MODIFIED
@app.route('/donations_history/<username>', methods=['GET','POST'])
def donationshistory(username):
    return render_template("donationshistory.html")

if __name__ == '__main__':
    app.secret_key = 'not-so-secret-key'
    app.run(debug=True)


