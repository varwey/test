#!/usr/bin/env python2.7
#coding:utf8

"""
filename: models.py
content: database model for user and message

2014/06/23 by varwey 
"""

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, aliased
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

engine = create_engine('sqlite:///data.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(30))
    password = Column(String(20))
    
    messages = relationship('message', backref='user', cascade='all, delete, delete-orphan')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.password)

class Message(Base):
    __tablename__  = 'messages'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    msg_time = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title, content, msg_time):
        self.title = title
        self.content = content
        self.msg_time = msg_time

    def __repr__(self):
        return "<Message('%s', '%s', '%s')>" % (self.title, self.content, self.msg_time)

Base.metadata.create_all(engine)

