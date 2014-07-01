# -*- coding=utf-8 -*-
from flask import request, abort, redirect
from flask.ext.login import LoginManager, login_url
from flask.ext.babel import gettext as _
from nowdo.controls.account import Account
from nowdo.utils.session import get_main_session

__author__ = 'zou'


_login_manager = LoginManager()
_login_manager.login_view = 'account.login'
_login_manager.login_message = _(u'请登录')


def init_app(app):
    _login_manager.init_app(app)


@_login_manager.user_loader
def user_loader(user_id):
    session = get_main_session()
    account = session.query(Account).get(user_id)
    return account


@_login_manager.unauthorized_handler
def unauthorized():
    if request.is_xhr or not _login_manager.login_view:
        abort(401)
    return redirect(login_url(_login_manager.login_view, request.url))