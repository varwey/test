# coding=utf-8
"""
created by SL on 14-3-10
"""
from functools import wraps
from flask import current_app, request, jsonify, redirect, url_for, flash
from flask.ext.login import current_user
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.group import Group
from nowdo.utils.session import session_cm

__author__ = 'SL'


def ajax_login_required(ajax_only=True):
    """
    ajax_only:
        True: 该view只接受ajax请求
        False: 该View接受ajax请求和非ajax请求，如果是ajax请求会传递 req_type = 'ajax' 参数
    """
    def wrapper(func):
        @wraps(func)
        def wrapped_view(*args, **kwargs):
            res = {
                'status': 'fail',
                'category': 'info',
                'info': u'not_login'
            }
            if not current_user.is_authenticated():
                if ajax_only or (not ajax_only and request.args.get('req_type') == 'ajax'):
                    return jsonify(res)
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return wrapped_view
    return wrapper


def group_admin_required(func):
    @wraps(func)
    def wrapped_view(*args, **kwargs):
        group_id = kwargs.get('group_id')
        with session_cm() as db_session:
            group = db_session.query(Group).get(group_id)
            if not group.is_admin(current_user):
                flash(u'只有小组的管理员才有此权限', 'info')
                return redirect(url_for('group.group_home', group_id=group_id))
        return func(*args, **kwargs)
    return wrapped_view


def task_admin_required(func):
    @wraps(func)
    def wrapped_view(*args, **kwargs):
        task_id = kwargs.get('task_id') or request.args.get('task_id')
        with session_cm() as db_session:
            task = db_session.query(CrowdSourceTask).get(task_id)
            if (task.group and task.group.is_admin(current_user)) or task.creator_id == current_user.id:
                return func(*args, **kwargs)
            flash(u'只有管理员才有此权限', 'info')
            return redirect(url_for('frontend.index'))
    return wrapped_view