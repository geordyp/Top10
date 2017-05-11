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
    return render_template('homescreen.html', categories=data)


@app.route('/top10/category/<string:category_url>')
def showCategory(category_url):
    """ Display category page with all top ten lists """
    # retrieve data
    listCategory = session.query(Category).filter_by(url=category_url).one()
    allLists = session.query(List).filter_by(category_id=listCategory.id).order_by(asc(List.date_created)).all()
    allListsWithItems = []
    for l in allLists:
        listItems = session.query(ListItem).filter_by(list_id=l.id).order_by(asc(ListItem.position)).all()
        if (len(listItems) > 2):
            allListsWithItems.append(listItems)

    return render_template('categorytable.html',
                           listsWithItems=allListsWithItems)


@app.route('/top10/category/<string:category_url>/list/new')
def createTopTenList(category_url):
    """ Create a new top ten list for the given category """
    listCategory = session.query(Category).filter_by(url=category_url).one()

    # TODO replace user_account_id=1 with currently logged in user

    # check if a list in this category has already been created by this user
    existingList = session.query(List).filter_by(category_id=listCategory.id, user_account_id=1).all()
    list_id = ""
    if (existingList):
        # if so, edit the exisiting list
        list_id = str(existingList[0].id)
    else:
        # if not, create a new list and edit
        newTopTenList = List(user_account_id=1,
                             category_id=listCategory.id)
        session.add(newTopTenList)
        session.commit()
        list_id = str(newTopTenList.id)

    return redirect(url_for('editTopTenList',
                            list_id=list_id))


@app.route('/top10/list/<string:list_id>/edit')
def editTopTenList(list_id):
    topTenList = session.query(List).filter_by(id=list_id).one()
    return render_template('edit_list.html',
                           list=topTenList)


@app.route('/top10/list/<string:list_id>/item/new')
def createListItem(list_id):
    return render_template('new_list.html', id=list_id)


if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=2077)
