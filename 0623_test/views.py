#!/usr/bin/env python2.7
#coding:utf8

"""
filename: views.py
content: handel view for user and messages of user

2014/06/23 by varwey
"""

from __future__ import with_statement
from contextlib import closing

#from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from database.models import User, Message


from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import View


app = Flask(__name__)

@app.before_request
def before_request():
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    g.db = Session()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        pass

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    g.db = Session()
    a = g.db.query(User).one()
    print a
