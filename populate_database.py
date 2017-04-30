from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, UserAccount, Category, ListItem, List

engine = create_engine('postgresql://me:password@localhost/top10')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create users
user1 = UserAccount(name="admin", id="1")
session.add(user1)
session.commit()

user2 = UserAccount(name="Bob", id="2")
session.add(user2)
session.commit()

user3 = UserAccount(name="Paul", id="3")
session.add(user3)
session.commit()


# Create categories
category1 = Category(name="Video Games",
                     url="TopTenVideogames",
                     public="true",
                     user_account_id="1")
session.add(category1)
session.commit()

category2 = Category(name="Movies",
                     url="TopTenMovies",
                     public="true",
                     user_account_id="1")
session.add(category2)
session.commit()

category3 = Category(name="Albums",
                     url="TopTenAlbums",
                     public="true",
                     user_account_id="1")
session.add(category3)
session.commit()

category4 = Category(name="Foods",
                     url="TopTenFoods",
                     public="true",
                     user_account_id="1")
session.add(category4)
session.commit()

category5 = Category(name="Books",
                     url="TopTenBooks",
                     public="true",
                     user_account_id="1")
session.add(category5)
session.commit()

category6 = Category(name="Cities",
                     url="TopTenCities",
                     public="true",
                     user_account_id="1")
session.add(category6)
session.commit()


# Create lists
list1 = List(user_account_id="2",
             category_id="1",
             id="1")
session.add(list1)
session.commit()

list2 = List(user_account_id="3",
             category_id="1",
             id="2")
session.add(list2)
session.commit()


# Create list items
listItem1 = ListItem(list_id="1",
                     position="1",
                     title="Mario")
session.add(listItem1)
session.commit()

listItem2 = ListItem(list_id="1",
                     position="2",
                     title="Mario")
session.add(listItem2)
session.commit()

listItem3 = ListItem(list_id="1",
                     position="3",
                     title="Mario")
session.add(listItem3)
session.commit()

listItem4 = ListItem(list_id="1",
                     position="4",
                     title="Mario")
session.add(listItem4)
session.commit()

listItem5 = ListItem(list_id="1",
                     position="5",
                     title="Mario")
session.add(listItem5)
session.commit()

listItem6 = ListItem(list_id="1",
                     position="6",
                     title="Mario")
session.add(listItem6)
session.commit()

listItem7 = ListItem(list_id="1",
                     position="7",
                     title="Mario")
session.add(listItem7)
session.commit()

listItem8 = ListItem(list_id="1",
                     position="8",
                     title="Mario")
session.add(listItem8)
session.commit()

listItem9 = ListItem(list_id="1",
                     position="9",
                     title="Mario")
session.add(listItem9)
session.commit()

listItem10 = ListItem(list_id="1",
                      position="10",
                      title="Mario")
session.add(listItem10)
session.commit()

listItem11 = ListItem(list_id="2",
                      position="1",
                      title="Matrix")
session.add(listItem11)
session.commit()

listItem12 = ListItem(list_id="2",
                      position="2",
                      title="Matrix")
session.add(listItem12)
session.commit()

listItem13 = ListItem(list_id="2",
                      position="3",
                      title="Matrix")
session.add(listItem13)
session.commit()

listItem14 = ListItem(list_id="2",
                      position="4",
                      title="Matrix")
session.add(listItem14)
session.commit()

listItem15 = ListItem(list_id="2",
                      position="5",
                      title="Matrix")
session.add(listItem15)
session.commit()

listItem16 = ListItem(list_id="2",
                      position="6",
                      title="Matrix")
session.add(listItem16)
session.commit()

listItem17 = ListItem(list_id="2",
                      position="7",
                      title="Matrix")
session.add(listItem17)
session.commit()

listItem18 = ListItem(list_id="2",
                      position="8",
                      title="Matrix")
session.add(listItem18)
session.commit()

listItem19 = ListItem(list_id="2",
                      position="9",
                      title="Matrix")
session.add(listItem19)
session.commit()

listItem20 = ListItem(list_id="2",
                      position="10",
                      title="Matrix")
session.add(listItem20)
session.commit()

print "populated the database!"
