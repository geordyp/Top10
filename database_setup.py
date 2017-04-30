from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import types

import datetime

Base = declarative_base()


class UserAccount(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=True)
    pwHash = Column(String(250), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    description = Column(String(500), nullable=True)
    public = Column(Boolean, nullable=False)
    user_account_id = Column(Integer, ForeignKey('user_account.id'), nullable=False)
    user_account = relationship(UserAccount)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'public': self.public,
            'userAccountID': self.user_account_id,
            'dateCreated': self.date_created
        }


class List(Base):
    __tablename__ = 'list'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship(Category)
    user_account_id = Column(Integer, ForeignKey('user_account.id'), nullable=False)
    user_account = relationship(UserAccount)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'userAccountID': self.user_account_id,
            'dateCreated': self.date_created
        }


class ListItem(Base):
    __tablename__ = 'list_item'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('list.id'), nullable=False)
    list = relationship(List)
    position = Column(Integer, nullable=False)
    title = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)
    img_url = Column(String(250), nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'listID': self.list_id,
            'position': self.position,
            'title': self.title,
            'description': self.description,
            'imgURL': self.img_url
        }


engine = create_engine('sqlite:///top10.db')
Base.metadata.create_all(engine)
