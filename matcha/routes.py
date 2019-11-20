from matcha import app, socket, db
from flask import render_template, redirect, url_for, request, flash, session
from matcha.forms import registration_validate
from functools import wraps


logged_in_users = []

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('username') is None:
            flash("Please login in first", 'info')
            return redirect( url_for('login', next=request.url))
        return f(*args, **kwargs)
    return wrapper



@app.route("/")
def home():
    return render_template("home.html", logged_in=session.get('logged_in'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # Get all the users information
    user = db.get_information(session.get('username'))
    if request.method == 'POST':
        username = request.form.get('userName')

        if username != user['username']:
            if not db.run_ret('SELECT * FROM users WHERE username=?', (username,)):
                db.run('UPDATE users SET username=? WHERE id=?', (username, user['id']))
                session['username'] = username
                return redirect( url_for("account"))
            else:
                flash("The user name is already taken, Try another", "danger")
    return render_template("account.html", user=user, logged_in=session.get('logged_in'))


@app.route("/logout")
@login_required
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect( url_for('home') )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if db.user_exists(username, password):
            flash("login successful", 'success')
            session['logged_in'] = True
            session['username'] = username
            logged_in_users.append(username)
            return redirect( url_for("home") )
        else:
            flash("Invalid user name/email.", 'danger')
    return render_template('login.html')

        
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        errors = registration_validate()

        if not errors:
            username = request.form.get('userName')            
            email = request.form.get('email')
            password = request.form.get('password')
            lastName = request.form.get('lastName')
            firstName = request.form.get('firstName')
            db.add_user(username, email, password, firstName,lastName)
            flash("You have successfully logged in!", 'success')

            return redirect(url_for('login'))
        else:
            for error in errors:
                flash(error, "danger")
    
    return render_template("register.html")