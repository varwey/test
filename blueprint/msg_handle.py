#!/usr/bin/python
#coding:utf8

from flask import Blueprint

app = Blueprint('msg_handle', __name__)

@app.route('/post')
def user_post():
    return 'This is User_post'

@app.route('/replay')
def user_replay():
    return 'This is User_replay'
