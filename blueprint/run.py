#!/usr/bin/python
#coding:utf8

from flask import Flask

import user_handle
import msg_handle

app = Flask(__name__)

app.register_blueprint(user_handle.app, url_prefix='/user_handle')
app.register_blueprint(msg_handle.app, url_prefix='/msg_handle')

if "__main__" == __name__:
    app.run(debug=True)

