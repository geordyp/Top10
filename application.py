from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from database_setup import Base, UserAccount, Category, ListItem, List

from functools import wraps

import string
import random
import json
import httplib2
import requests

app = Flask(__name__)

APPLICATION_NAME = 'Top 10'

engine = create_engine('sqlite:///top10.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/top10')
def showHome():
    """ Show the home page """
    data = session.query(Category).all()
    return render_template('homescreen.html', category=data)


@app.route('/top10/<string:category_url>')
def showCategory(category_url):
    """ Display category page with all top ten lists """
    # retrieve data
    category = session.query(Category).filter_by(url=category_url).one()
    allLists = session.query(List).filter_by(category_id=category.id).order_by(asc(List.date_created)).all()
    allListsWithItems = []
    for l in allLists:
        listItems = session.query(ListItem).filter_by(list_id=l.id).order_by(asc(ListItem.position)).all()
        allListsWithItems.append(listItems)

    return render_template('test-lists.html', listsWithItems=allListsWithItems)


if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=2077)
