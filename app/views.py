""" This module contains all the view functions for the bucketlist app"""
import re

from models import User

USERS = {}
USERS['eric.elem'] = User('Eric Elem', 'eric.elem', 'password')

def register(name, username, password):
    """ This function handles user registration"""
    if name and username and password:
        if name.strip() and username.strip and password.strip:
            if len(username) > 5 and len(username) < 11:
                if len(password) > 5 and len(password) < 11:
                    if re.match("^[a-zA-Z0-9_.-]+$", username):
                        return "Registration successful"
                    return "Username contains illegal characters"
                return "Password length should be from 6 to 10 characters"
            return "Username length should be from 6 to 10 characters"
        return "Blank input"
    return "None input"

def login(username, password):
    """ Handles user login """
    if username and password:
        if username.strip() and password.strip():
            if username in USERS:
                if USERS[username].password == password:
                    #session['username']=username
                    return "Login successful"
                return "Wrong password"
            return "User not found"
        return "Blank input"
    return "None input"
