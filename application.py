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
    # TODO 404 category not found
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
def newTopTenList(category_url):
    """ Create a new top ten list for the given category """
    # TODO 404 category not found
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
    """ Edit a top ten list """
    # TODO 404 list not found
    topTenList = session.query(List).filter_by(id=list_id).one()
    listItems = session.query(ListItem).filter_by(list_id=list_id).order_by(asc(ListItem.position)).all()

    canAddMoreItems = False
    if (len(listItems) < 10):
        canAddMoreItems = True

    return render_template('list_form.html',
                           listItems=listItems,
                           list=topTenList,
                           canAddMoreItems=canAddMoreItems,
                           error="")


@app.route('/top10/list/<string:list_id>/item/new', methods=['GET', 'POST'])
def newListItem(list_id):
    """ Create a new list item """
    # TODO 404 list not found
    topTenList = session.query(List).filter_by(id=list_id).one()

    listItems = session.query(ListItem).filter_by(list_id=list_id).order_by(asc(ListItem.position)).all()
    newItemPosition = -1
    if (len(listItems) < 10):
        newItemPosition = len(listItems) + 1
    else:
        return render_template('list_form.html',
                               listItems=listItems,
                               list=topTenList,
                               canAddMoreItems=False,
                               error="Can't create more than 10 items in your list")

    if request.method == 'GET':
        return render_template('listItem_form.html',
                               list=topTenList,
                               id="",
                               position=newItemPosition,
                               editing=False,
                               title="",
                               description="",
                               error="")
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
                                   error=error)


@app.route('/top10/item/<string:listItem_id>/edit', methods=['GET', 'POST'])
def editListItem(listItem_id):
    """ Edit a list item """
    # TODO 404 item not found
    editedListItem = session.query(ListItem).filter_by(id=listItem_id).one()

    if request.method == 'GET':
        return render_template('listItem_form.html',
                               list=editedListItem.list,
                               id=listItem_id,
                               position=editedListItem.position,
                               editing=True,
                               title=editedListItem.title,
                               description=editedListItem.description,
                               error="")
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
                                   error=error)

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
                                           error=error)
        else:
            error = "Please include a position."
            return render_template('listItem_form.html',
                                   list=editedListItem.list,
                                   id=listItem_id,
                                   position=request.form['position'],
                                   editing=True,
                                   title=request.form['title'],
                                   description=request.form['description'],
                                   error=error)

        session.add(editedListItem)
        session.commit()
        return redirect(url_for('editTopTenList', list_id=editedListItem.list_id))


@app.route('/top10/item/<string:listItem_id>/delete')
def deleteListItem(listItem_id):
    """ Delete a list item """
    # TODO 404 not found
    deletedListItem = session.query(ListItem).filter_by(id=listItem_id).one()

    # shift the remaining list items
    listItems = session.query(ListItem).filter_by(list_id=deletedListItem.list_id).order_by(asc(ListItem.position)).all()
    if deletedListItem.position != len(listItems):
        for i in range(deletedListItem.position - 1, len(listItems) - 1):
            listItems[i + 1].position = listItems[i + 1].position - 1

    session.delete(deletedListItem)
    session.commit()
    return redirect(url_for('editTopTenList', list_id=deletedListItem.list_id))



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=2077)
