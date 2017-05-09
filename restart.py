from flask import Flask,g, render_template, request, redirect, jsonify, url_for, flash
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
import os
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Item Catalog Project'
app = Flask(__name__)
app.secret_key = os.urandom(24)
@app.route('/', methods=['GET','POST'])
def login():
   if request.method =='POST':
      login_session.pop('user',None)

      if request.form['password'] == 'password':
		login_session['user'] = request.form['username']
		return redirect(url_for('home'))

  		
   return render_template('login.html')
 
@app.route('/home')
def home():
    if g.user:
         return render_template('home.html')
         
	
    return redirect(url_for('login'))
@app.before_request
def before_request():
     g.user = None
     if 'user' in login_session:
         g.user = login_session['user']

@app.route('/getsession')
def getsession():
    if 'user' in login_session:
        return login_session['user']
                 

    return 'Not logged in!'

@app.route('/dropsesssion')
def dropsession():
     login_session.pop('user',None)
     return 'Dropped!'

@app.route('/register')
def register():
   return render_template('register.html')
                 

if __name__ == '__main__':
     app.run(debug=True)


if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=2033)
