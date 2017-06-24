from flask import Flask, url_for, request, render_template, redirect, session, flash

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt #encrypting the password
#/changes
users_db = {'demo':sha256_crypt.encrypt('demo')}

app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    return render_template("index.html")


###########################################################changes#################################################
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        users_db[username] = password

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)
########################################## /changes ##############################################################
@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login_form', methods=['POST'])
def login_form():
    username = request.form['username']
    password = request.form['password']
    if username in users_db and sha256_crypt.verify(password, users_db[username]):
        session['logged_in_user'] = username
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error="Wrong credentials!")

@app.route('/logout')
def logout():
    del session['logged_in_user']
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'not-so-secret-key'
    app.run(debug=True)


