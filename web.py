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
mylist = [('https://uniqlo.scene7.com/is/image/UNIQLO/goods_08_126133?$pdp-medium$', 'Sweater to Donate!'), ('http://kyjaak.com/images/produits/f9c208b1ca20b0bfceefa4c21a94ec07.jpg', 'Flour bags to donate.'), ('http://az616578.vo.msecnd.net/files/2016/06/10/636011916262124344-1313810365_socks.jpg', 'Socks to give out.'), ('https://www.taylorguitars.com/sites/default/files/browse-guitars-600-500x647.jpg', 'Guitar for beginners'), ('http://cdn.decoist.com/wp-content/uploads/2013/08/Set-of-6-cordial-glasses.jpg', 'Set of glasses.') ]
app = Flask(__name__)
with app.test_request_context():
    app.config['UPLOAD_FOLDER_ACCOUNTS'] = "/static/accounts/"
    app.config['UPLOAD_FOLDER_DONATIONS'] = "/static/donations/"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = '3306'
app.config['MYSQL_DB'] = 'DONATIVA'
mysql = MySQL(app)
# mysql.init_app(app)

@app.route('/donation/<donation_id>')
def donation(donation_id):
    offer = mysql_connector.get_donation(mysql, donation_id)
    return render_template('donation.html', offer=offer, format_date_hour=helpers.format_date_hour, get_username=mysql_connector.get_username, mysql = mysql)

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
    if 'account_id' in session:
        args = session['account_id']
    else:
        args = 0 #dummy variable

    triplets= mysql_connector.generate_index(mysql, args)
    print(triplets)
    n_requests = mysql_connector.view_number_notifications(mysql,session['type'], args)
    myrequests = mysql_connector.view_notifications(mysql,session['type'], args)
    folder = os.path.join(app.config['UPLOAD_FOLDER_DONATIONS'])
    get_username = mysql_connector.get_username
    format_date = helpers.format_date
    return render_template("index.html", triplets=triplets, myrequests=myrequests, n_requests=n_requests[0][0], folder=folder, get_username=get_username, mysql=mysql, format_date=format_date)




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
            return redirect(url_for('index'))
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
        donation_date = form.donation_date.data.strftime('%y-%m-%d')
        file = request.files['file']
        if file.filename == '':
            filename = 'none.jpg'
        else:
            filename = secure_filename(file.filename)
        args = (session['account_id'], title, description, city, donation_type, donation_date, address, filename)
        offer_id = mysql_connector.add_donation(mysql, args)
        file_path = os.path.join(app.config['UPLOAD_FOLDER_DONATIONS'], str(offer_id) + '.jpg')
        if file.filename != '':
            helpers.upload_file(file, file_path)
        
        return redirect(url_for('index'))
    args = session['account_id']
    n_requests = mysql_connector.view_number_notifications(mysql,session['type'], args)
    myrequests = mysql_connector.view_notifications(mysql,session['type'], args) 
    return render_template('donation_add.html', form=form,myrequests=myrequests ,n_requests=n_requests[0][0])
        


# Authentication
@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")
    
@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
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
    args = session['account_id']
    myrequests = mysql_connector.get_requests(mysql,args) 
    n_requests = mysql_connector.get_number_requests(mysql,args)
    user = mysql_connector.get_user(mysql, username)
    user_type = mysql_connector.get_type_user(mysql, username)
    if user_type == 1:
        triplets = mysql_connector.get_donor_donations(mysql, user[0])
    else:
        triplets = mysql_connector.get_organization_donations(mysql, user[0])
    triplets = helpers.group_list(triplets, 2)
    folder = os.path.join(app.config['UPLOAD_FOLDER_DONATIONS'])
    get_username = mysql_connector.get_username
    format_date = helpers.format_date
    return render_template("profile.html", get_username=get_username, format_date=format_date,mysql=mysql,folder=folder, user=user, triplets=triplets, myrequests=myrequests, n_requests=n_requests[0][0])


@app.route('/myrequests', methods=['GET','POST'])
def myrequests():
    args = session['account_id']
    myrequests = mysql_connector.get_requests(mysql,args)
    n_requests = mysql_connector.get_number_requests(mysql,args)
    return render_template("myrequests.html", myrequests=myrequests, n_requests=n_requests[0][0])


@app.route('/process_requests/<status>/<requester_id>/<offer_id>', methods=['GET','POST'])
def process_requests(offer_id, requester_id, status):
    args = (offer_id, requester_id)
    if status == '-1': #cancel this request
        mysql_connector.cancel_request(mysql,args)
    else:
        mysql_connector.accept_request(mysql,args)
    return(redirect(url_for('myrequests')))


@app.route('/send_requests/<account_id>/<offer_id>', methods=['GET','POST'])
def send_requests(account_id, offer_id):
    args = (account_id,offer_id)
    mysql_connector.send_request(mysql,args)
    return(redirect(url_for('index')))

@app.route('/myanswers', methods=['GET','POST'])
def myanswers():
    args = session['account_id']
    n_requests = mysql_connector.view_number_notifications(mysql,session['type'], args)
    myrequests = mysql_connector.view_notifications(mysql,session['type'], args)
    return render_template("myanswers.html", myrequests=myrequests, n_requests=n_requests[0][0])


if __name__ == '__main__':
    app.secret_key = 'not-so-secret-key'
    app.run(debug=True)


