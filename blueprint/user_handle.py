#!/usr/bin/python
#coding:utf8

"""
a test of blueprint
2014/06/30 by varwey
"""

from flask import Blueprint

app = Blueprint('user_handel', __name__)

@app.route('/login')
def user_login():
    return 'This is User_login'

@app.route('/logout')
def user_logout():
    return 'This is User_logout'
