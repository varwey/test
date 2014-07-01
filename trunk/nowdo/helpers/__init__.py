# coding=utf-8
"""
created by SL on 14-3-11
"""
from flask import g
from nowdo.controls.group import Group
from nowdo.utils.session import session_cm

__author__ = 'SL'


def pull_current_group(endpoint, values):
    pass
    # group_id = values.get('group_id')
    # if group_id:
    #     with session_cm() as db_session:
    #         g.group = db_session.query(Group).get(group_id)