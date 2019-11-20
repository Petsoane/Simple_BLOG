from flask import request
from matcha import db


def registration_validate():
    # errors = {
    #     'username': [],
    #     'email': [],
    #     'password':[],
    #     'password_confirm': []
    # }
    errors = []
    # validate the password
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    username = request.form.get('userName')
    email = request.form.get('email')

    if len(password)  < 8:
        errors.append("The password is too short")
    if password_confirm != password:
        errors.append("The two passwords dont match")
    if (not db.usename_unique(username)):
        errors.append("The user name is already taken, please chose another one")
    if (not db.email_unique(email)):
        errors.append("The email is already taken, please chose another one") 
    return None if not len(errors) else errors
