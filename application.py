from flask import Flask,g, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from database_setup import Base, UserAccount, Category, ListItem, List

from functools import wraps
from database_setup import Base, UserAccount,Category, ListItem, List
import string
import random
import json
import httplib2
import requests
import hashlib

app = Flask(__name__)



APPLICATION_NAME = 'Top 10'

engine = create_engine('sqlite:///top10.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

APPLICATION_NAME = 'Item Catalog Project'
app = Flask(__name__)


@app.route('/')
def home():
    if not login_session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('showHome'))


@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    phash = hashlib.sha256(POST_PASSWORD).hexdigest()
    user = session.query(UserAccount).filter_by(name=POST_USERNAME, pwHash=phash).all()
    if user:
       login_session['logged_in'] = True
       login_session['user_id'] = user[0].id
       return redirect(url_for('home'))
    else:
        error = "Incorrect username or password."
        return render_template('login.html',
                               error=error)


@app.route("/logout")
def logout():
    login_session['logged_in'] = False
    login_session['user_id'] = -1
    return redirect(url_for('home'))


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        name = request.form['username']
        password = request.form['pwd']
        pwd = hashlib.sha256(password).hexdigest()

        result = session.query(UserAccount).filter_by(name=name).all()
        if result:
            error = "That username is taken."
            return render_template('register.html', error=error)

        newUser = UserAccount(name=name,
                              email=email,
                              pwHash=pwd)
        session.add(newUser)
        session.commit()
        return redirect(url_for('home'))


@app.route('/top10')
def showHome():
    """ Show the home page """
    data = session.query(Category).all()
    return render_template('homescreen.html',
                           categories=data,
                           logged_in=login_session.get('logged_in'))


@app.route('/top10/category/<string:category_url>')
def showCategory(category_url):
    """ Display category page with all top ten lists """
    try:
        listCategory = session.query(Category).filter_by(url=category_url).one()
    except NoResultFound:
        abort(404)

    allLists = session.query(List).filter_by(category_id=listCategory.id).order_by(desc(List.date_created)).all()
    allListsWithItems = []
    for l in allLists:
        if l.user_account_id != 1:
            listItems = session.query(ListItem).filter_by(list_id=l.id).order_by(asc(ListItem.position)).all()
            if (len(listItems) > 4):
                allListsWithItems.append(listItems)
    return render_template('categorytable.html',
                           listsWithItems=allListsWithItems,
                           categoryTitle=listCategory.name,
                           categoryUrl=listCategory.url,
                           logged_in=login_session.get('logged_in'))


@app.route('/top10/category/<string:category_url>/list/new')
def newTopTenList(category_url):
    """ Create a new top ten list for the given category """
    if not login_session.get('logged_in'):
        return redirect(url_for('home'))

    try:
        listCategory = session.query(Category).filter_by(url=category_url).one()
    except NoResultFound:
        abort(404)

    # check if a list in this category has already been created by this user
    existingList = session.query(List).filter_by(category_id=listCategory.id, user_account_id=login_session.get('user_id')).all()
    list_id = ""
    if (existingList):
        # if so, edit the exisiting list
        list_id = str(existingList[0].id)
    else:
        # if not, create a new list and edit
        newTopTenList = List(user_account_id=login_session.get('user_id'),
                             category_id=listCategory.id)
        session.add(newTopTenList)
        session.commit()
        list_id = str(newTopTenList.id)

    return redirect(url_for('editTopTenList',
                            list_id=list_id))


@app.route('/top10/list/<string:list_id>/edit')
def editTopTenList(list_id):
    """ Edit a top ten list """
    if not login_session.get('logged_in'):
        return redirect(url_for('home'))

    try:
        topTenList = session.query(List).filter_by(id=list_id).one()
    except NoResultFound:
        abort(404)

    listItems = session.query(ListItem).filter_by(list_id=list_id).order_by(asc(ListItem.position)).all()

    # check if the user created the list they're about to edit
    if login_session.get('user_id') != topTenList.user_account_id:
        return redirect(url_for('showCategory',
                                category_url=topTenList.category.url))

    canAddMoreItems = False
    if (len(listItems) < 10):
        canAddMoreItems = True

    return render_template('list_form.html',
                           listItems=listItems,
                           listLength=len(listItems),
                           list=topTenList,
                           canAddMoreItems=canAddMoreItems,
                           error="",
                           logged_in=login_session.get('logged_in'))


@app.route('/top10/list/<string:list_id>/item/new', methods=['GET', 'POST'])
def newListItem(list_id):
    """ Create a new list item """
    if not login_session.get('logged_in'):
        return redirect(url_for('home'))

    try:
        topTenList = session.query(List).filter_by(id=list_id).one()
    except NoResultFound:
        abort(404)

    # check if the user created the list they're about to edit
    if login_session.get('user_id') != topTenList.user_account_id:
        return redirect(url_for('showCategory',
                                category_url=topTenList.category.url))

    listItems = session.query(ListItem).filter_by(list_id=list_id).order_by(asc(ListItem.position)).all()
    newItemPosition = -1
    if (len(listItems) < 10):
        newItemPosition = len(listItems) + 1
    else:
        return render_template('list_form.html',
                               listItems=listItems,
                               list=topTenList,
                               canAddMoreItems=False,
                               error="Can't create more than 10 items in your list",
                               logged_in=login_session.get('logged_in'))

    if request.method == 'GET':
        return render_template('listItem_form.html',
                               list=topTenList,
                               id="",
                               position=newItemPosition,
                               editing=False,
                               title="",
                               description="",
                               error="",
                               logged_in=login_session.get('logged_in'))
    else:
        if request.form['title']:
            newItem = ListItem(list_id=list_id,
                               position=newItemPosition,
                               title=request.form['title'],
                               description=request.form['description'])
            session.add(newItem)
            session.commit()
            return redirect(url_for('editTopTenList', list_id=list_id))
        else:
            error = "Please include a title."
            return render_template('listItem_form.html',
                                   list=topTenList,
                                   id="",
                                   position=newItemPosition,
                                   editing=False,
                                   title=request.form['title'],
                                   description=request.form['description'],
                                   error=error,
                                   logged_in=login_session.get('logged_in'))


@app.route('/top10/item/<string:listItem_id>/edit', methods=['GET', 'POST'])
def editListItem(listItem_id):
    """ Edit a list item """
    if not login_session.get('logged_in'):
        return redirect(url_for('home'))

    try:
        editedListItem = session.query(ListItem).filter_by(id=listItem_id).one()
    except NoResultFound:
        abort(404)

    # check if the user created the list they're about to edit
    if login_session.get('user_id') != editedListItem.list.user_account_id:
        return redirect(url_for('showCategory',
                                category_url=editedListItem.list.category.url))

    if request.method == 'GET':
        return render_template('listItem_form.html',
                               list=editedListItem.list,
                               id=listItem_id,
                               position=editedListItem.position,
                               editing=True,
                               title=editedListItem.title,
                               description=editedListItem.description,
                               error="",
                               logged_in=login_session.get('logged_in'))
    else:
        if request.form['title']:
            editedListItem.title = request.form['title']
        else:
            error = "Please include a title."
            return render_template('listItem_form.html',
                                   list=editedListItem.list,
                                   id=listItem_id,
                                   position=request.form['position'],
                                   editing=True,
                                   title=request.form['title'],
                                   description=request.form['description'],
                                   error=error,
                                   logged_in=login_session.get('logged_in'))

        editedListItem.description = request.form['description']

        if request.form['position']:
            newItemPosition = int(request.form['position'])
            if newItemPosition != editedListItem.position:
                if newItemPosition > 0 and newItemPosition < 11:
                    listItems = session.query(ListItem).filter_by(list_id=editedListItem.list_id).order_by(asc(ListItem.position)).all()
                    if len(listItems) < newItemPosition:
                        swapListItem = session.query(ListItem).filter_by(list_id=editedListItem.list_id, position=len(listItems)).order_by(asc(ListItem.position)).one()
                        swapListItem.position = editedListItem.position
                        editedListItem.position = newItemPosition
                        session.add(swapListItem)
                    else:
                        swapListItem = session.query(ListItem).filter_by(list_id=editedListItem.list_id, position=newItemPosition).order_by(asc(ListItem.position)).one()
                        swapListItem.position = editedListItem.position
                        editedListItem.position = newItemPosition
                        session.add(swapListItem)
                else:
                    error = "Position needs to be between 1 and 10."
                    return render_template('listItem_form.html',
                                           list=editedListItem.list,
                                           id=listItem_id,
                                           position=request.form['position'],
                                           editing=True,
                                           title=request.form['title'],
                                           description=request.form['description'],
                                           error=error,
                                           logged_in=login_session.get('logged_in'))
        else:
            error = "Please include a position."
            return render_template('listItem_form.html',
                                   list=editedListItem.list,
                                   id=listItem_id,
                                   position=request.form['position'],
                                   editing=True,
                                   title=request.form['title'],
                                   description=request.form['description'],
                                   error=error,
                                   logged_in=login_session.get('logged_in'))

        session.add(editedListItem)
        session.commit()
        return redirect(url_for('editTopTenList', list_id=editedListItem.list_id))


@app.route('/top10/item/<string:listItem_id>/delete')
def deleteListItem(listItem_id):
    """ Delete a list item """
    if not login_session.get('logged_in'):
        return redirect(url_for('home'))

    try:
        deletedListItem = session.query(ListItem).filter_by(id=listItem_id).one()
    except NoResultFound:
        abort(404)

    # check if the user created the list they're about to edit
    if login_session.get('user_id') != deletedListItem.list.user_account_id:
        return redirect(url_for('showCategory',
                                category_url=deletedListItem.list.category.url))

    # shift the remaining list items
    listItems = session.query(ListItem).filter_by(list_id=deletedListItem.list_id).order_by(asc(ListItem.position)).all()
    if deletedListItem.position != len(listItems):
        for i in range(deletedListItem.position - 1, len(listItems) - 1):
            listItems[i + 1].position = listItems[i + 1].position - 1

    session.delete(deletedListItem)
    session.commit()
    return redirect(url_for('editTopTenList', list_id=deletedListItem.list_id))


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html',
                           logged_in=login_session.get('logged_in'))


if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=2077)
