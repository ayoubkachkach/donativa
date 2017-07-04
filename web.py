from flask import Flask, url_for, request, render_template, redirect, session, flash
from passlib.hash import sha256_crypt #encrypting the password
from flask_mysqldb import MySQL
import forms

from functools import wraps

users_db = {'demo':sha256_crypt.encrypt('demo')}
triplets = [[1,2,3], [1,2,3], [1,2,3], [1,2]]

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'azerty'
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
    return render_template("index.html", triplets=triplets)

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
@login_required
def logout():
    del session['logged_in_user']
    return redirect('/')

@app.route('/login_form', methods=['POST'])
def login_form():
    username = request.form['username']
    password = request.form['password']
    # Create cursor
    cur = mysql.connection.cursor()
    # Get user by username
    result = cur.execute("SELECT * FROM ACCOUNTS WHERE account_username = %s ", [username])
    if result > 0:
        # Get stored hash
        data = cur.fetchone()
        password = data['password']
        # Compare Passwords
        if sha256_crypt.verify(password_candidate, password):
            # Passed
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index')) 
        else:
            return render_template('login.html', error="Wrong credentials!")
        # Close connection
        cur.close()
    else:
        return render_template('login.html', error="Wrong credentials!")
        # Close connection
        cur.close()
    cur.close()
#Profile
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    return render_template("profile.html", username=username)

#TO BE MODIFIED
@app.route("/donationshistory", methods=['GET','POST'])
def donationshistory():
    return render_template("donationshistory.html")

if __name__ == '__main__':
    app.secret_key = 'not-so-secret-key'
    app.run(debug=True)


