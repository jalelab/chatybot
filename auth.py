# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username= request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        error = 'Invalid Credentials. Please try again.'
        return render_template('login.html', error =error) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.admin'))

@auth.route("/settings", methods=['GET','POST'])
@login_required
def settings():
    if request.method=='POST':
        JsonData=request.get_json()
        username=JsonData.get('username')
        old_password=JsonData.get('current')
        new_password=JsonData.get('new')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, old_password) :
            return ("check your username or current password")
        if len(new_password)<5:
            return ("new password must be 5 characters at least")
        user.password = generate_password_hash(new_password, method='sha256')
        print(generate_password_hash(new_password, method='sha256'))
        db.session.commit()
        print(user.password)

        return "Password changed successfully"
    return render_template("settings.html")

@auth.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('main.index'))
