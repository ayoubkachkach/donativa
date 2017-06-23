from flask import Flask, url_for, request, render_template, redirect

users_db = {'ayoub':'azerty', 'manal':'qwerty', 'nisrine':'SW<3', 'abdelmajid':'saykouk'}

app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=['GET'])
def login():
	return render_template("login.html")

@app.route('/login_form', methods=['POST'])
def login_form():
	email = request.form['email']
	password = request.form['password']
	if password == users_db.get(email):
		return redirect(url_for('profile', name=request.form['email']))
	else:
		return render_template('login.html', error="Wrong credentials!")

@app.route('/profile/<name>')
def profile(name):
	date = "29/12/1997"
	age = 19
	return render_template("index.html", name=name, age=age, date=date)



