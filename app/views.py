""" This module contains all the view functions for the bucketlist app"""
import re
from functools import wraps
from app import APP
from flask import render_template, session, flash, redirect, url_for, request
from models import User

USERS = {}

def register(name, username, password, rpt_password):
    """ This function handles user registration"""
    if name and username and password and rpt_password:
        if name.strip() and username.strip() and password.strip() and rpt_password.strip():
            if len(username) > 3 and len(username) < 11:
                if re.match("^[a-zA-Z0-9_.-]+$", username):
                    if len(password) > 5 and len(password) < 11:
                        if password == rpt_password:
                            USERS[username] = User(name, username, password)
                            return "Registration successful"
                        return "Passwords don't match"
                    return "Password should be 6 to 10 characters"
                return "Illegal characters in username"
            return "Username should be 4 to 10 characters"
        return "Blank input"
    return "None input"

def login(username, password):
    """ Handles user login """
    if username and password:
        if username.strip() and password.strip():
            if USERS.get(username):
                if USERS[username].password == password:
                    return "Login successful"
                return "Wrong password"
            return "User not found"
        return "Blank input"
    return "None input"


@APP.route('/')
def index():
    """ Handles the index route """
    if session.get('username'):
        return redirect(url_for('read_buckets'))
    else:
        return redirect(url_for('sign_in'))

@APP.route('/sign_in', methods=['GET','POST'])
def sign_in():
    """ Handles the sign_in route """
    if request.method == 'POST':
        result = login(request.form['username'], request.form['password'])
        if result == "Login successful":
            session['username'] = request.form['username']
            return redirect(url_for('read_buckets'))
        flash(result, 'warning')
    return render_template('login.html')

@APP.route('/sign_up', methods=['GET','POST'])
def sign_up():
    """ Handles the sign_up route """
    if request.method == 'POST':
        result = register(request.form['name'], request.form['username'], request.form['password']
                          , request.form['rpt_password'])
        if result == "Registration successful":
            flash(result, 'info')
            return redirect(url_for('sign_in'))
        flash(result, 'warning')
    return render_template('register.html')

def login_required(func):
    """ Decorator function to ensure some routes are only accessed by logged in users """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """ Modified descriprition of the decorated function """
        if not session.get('username'):
            flash('Login to continue', 'warning')
            return redirect(url_for('sign_in', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

@APP.route('/read_buckets', methods=['GET', 'POST'])
@login_required
def read_buckets():
    """ Handles displaying buckets """
    return render_template('buckets/read.html', buckets=USERS[session['username']].buckets)

@APP.route('/create_bucket', methods=['GET', 'POST'])
@login_required
def create_bucket():
    """ Handles new bucket creation requests """
    if request.method == 'POST':
        result = USERS[session['username']].add_bucket(request.form['title'])
        if result == 'Bucket added':
            flash(result, 'info')
        else:
            flash(result, 'warning')
        return redirect(url_for('read_buckets'))
    return render_template('buckets/create.html')

@APP.route('/update_bucket/<title>', methods=['GET', 'POST'])
@login_required
def update_bucket(title):
    """ Handles request to update a bucket """
    session['bucket_title'] = title
    if request.method == 'POST':
        result = USERS[session['username']].update_bucket(session['bucket_title'],
                                                          request.form['title'])
        if result == 'Bucket updated':
            flash(result, 'info')
        else:
            flash(result, 'warning')
        return redirect(url_for('read_buckets'))
    return render_template('buckets/update.html')

@APP.route('/delete_bucket/<title>',methods=['GET', 'POST'])
@login_required
def delete_bucket(title):
    """ Handles request to delete a bucket """
    result = USERS[session['username']].delete_bucket(title)
    if result == 'Bucket deleted':
        flash(result, 'info')
    else:
        flash(result, 'warning')
    return redirect(url_for('read_buckets'))

@APP.route('/read_items/<bucket_title>', methods=['GET', 'POST'])
@login_required
def read_items(bucket_title):
    """ Handles displaying items """
    session['current_bucket_title'] = bucket_title
    return render_template('items/read.html', items=USERS[session['username']]
                           .buckets[bucket_title].items)

@APP.route('/create_item',methods=['GET', 'POST'])
@login_required
def create_item():
    """ Handles new item creation requests """
    if request.method == 'POST':
        result = USERS[session['username']].buckets[session['current_bucket_title']].add_item(
            request.form['description'])
        if result == 'Item added':
            flash(result, 'info')
        else:
            flash(result, 'warning')
        return redirect(url_for('read_items', bucket_title=session['current_bucket_title']))
    return render_template('items/create.html', items=USERS[session['username']]
                           .buckets[session['current_bucket_title']].items)

@APP.route('/update_item/<description>',methods=['GET', 'POST'])
@login_required
def update_item(description):
    """ Handles request to update an item """
    session['description'] = description
    if request.method == 'POST':
        des_result = (USERS[session['username']].buckets[session['current_bucket_title']].
                      update_description(session['description'], request.form['description']))
        status_result = (USERS[session['username']].buckets[session['current_bucket_title']].
                         update_status(session['description'], request.form['status']))
        if des_result == 'Item updated' or status_result == 'Item updated':
            flash('Item updated', 'info')
        else:
            flash(des_result, 'warning')
        return redirect(url_for('read_items', bucket_title=session['current_bucket_title']))
    return render_template('items/update.html', item=USERS[session['username']]
                           .buckets[session['current_bucket_title']].items[description],
                           items=USERS[session['username']].
                           buckets[session['current_bucket_title']].items)

@APP.route('/delete_item/<description>',methods=['GET', 'POST'])
@login_required
def delete_item(description):
    """ Handles request to delete an item """
    result = USERS[session['username']].buckets[session['current_bucket_title']].delete_item(
        description)
    if result == 'Item deleted':
        flash(result, 'info')
    else:
        flash(result, 'warning')
    return redirect(url_for('read_items', bucket_title=session['current_bucket_title']))

@APP.route('/logout')
@login_required
def logout():
    """ logs out users """
    session.pop('username')
    flash('You have logged out', 'warning')
    return redirect(url_for('index'))
