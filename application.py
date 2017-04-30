from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from functools import wraps

import string
import random
import json
import httplib2
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Item Catalog Project'


@app.route('/')
@app.route('/top10')
def showHome():
    """ Show the home page """
    names = ["Movies", "The Shawshank Redemption", "Batman: The Dark Knight", "Lord of the Rings: Return of the King", "Avatar"]
    return render_template('homescreen.html', category=names)

if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=2077)
