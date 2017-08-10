""" Main module for the bucket list application """
from flask import Flask
APP = Flask(__name__)
APP.secret_key = 'SessionskeyForBucketListApp256'
from views import *

if __name__ == '__main__':
    APP.run()
    