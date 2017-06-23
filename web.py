from flask import Flask, url_for, request, render_template, redirect, session

users_db = {'ayoub':'azerty', 'demo': 'demo',
			'manal':'qwerty', 'nisrine':'SW<3',
			'abdelmajid':'saykouk'}

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

@app.route('/login', methods=['GET'])
def login():
	return render_template("login.html")

@app.route('/login_form', methods=['POST'])
def login_form():
	username = request.form['username']
	password = request.form['password']
	if password == users_db.get(username):
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


