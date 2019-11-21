from matcha import app, socket, db
from flask import render_template, redirect, url_for, request, flash, session
from matcha.forms import registration_validate
from werkzeug import secure_filename
from functools import wraps
from PIL import Image
import os, secrets




def save_picture(form_pic):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(secure_filename(form_pic.filename))
    pic_fn =  rand_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)

    # form_pic.save(pic_path)
    i = Image.open(form_pic.stream)
    i.thumbnail((200,200))

    i.save(pic_path)
    return pic_fn

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
    user = db.get_information(session.get('username'))
    return render_template("home.html", logged_in=session.get('logged_in'), user=user)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    errors = []
    # Get all the users information
    user = db.get_information(session.get('username'))
    print(user)
    if request.method == 'POST':
        username = request.form.get('userName')
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        image_file = request.files['image']

        if username != user['username']:
            if not db.run_ret('SELECT * FROM users WHERE username=?', (username,)):
                db.run('UPDATE users SET username=? WHERE id=?', (username, user['id']))
                session['username'] = username
                return redirect( url_for("account"))
            else:
                errors.append("The username is already taken")
        
        if email != user['email']:
            if not db.run_ret('SELECT * FROM users WHERE email=?', (email,)):
                db.run('UPDATE users SET email=? WHERE id=?', (email, user['id']))
                return redirect( url_for('account') )
            else:
                errors.append("The email is already taken")

        if firstname != user['name']:
            db.run('UPDATE users SET name=? WHERE id=?', (firstname, user['id']))
            return redirect( url_for('account') )

        if lastname != user['lastName']:
            db.run('UPDATE users SET lastName=? WHERE id=?', (lastname, user['id']))
            return redirect( url_for('account') )

        print(image_file)
        if image_file:
            pic_file = save_picture(image_file)
            print(pic_file)
            db.run('UPDATE users SET image_name=? WHERE id=?', (pic_file, user['id']))
            return redirect( url_for('account') )


        if errors:
            for error in errors:
                flash(error, "danger")
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