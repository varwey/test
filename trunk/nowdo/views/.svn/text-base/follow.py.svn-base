# coding=utf-8
"""
created by SL on 14-3-27
"""
import traceback
from flask import Blueprint, request, current_app, jsonify
from flask.ext.login import current_user
from nowdo.controls.follows import Follow
from nowdo.controls.account import Account
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm

__author__ = 'SL'

follow_bp = Blueprint('follow', __name__)


@follow_bp.route('/toggle_follow_user')
def toggle_follow_user():
    target_id = request.args.get('target_id')
    res = ajax_response()

    if not current_user.is_authenticated():
        res.update({
            'status': 'fail',
            'info': 'not_login'
        })
        return jsonify(res)

    if target_id:
        with session_cm() as account_session:
            user = account_session.query(Account).get(target_id)
            if user:
                try:
                    ret = Follow.toggle_follow(current_user, user)
                    res.update(info=ret)
                    return jsonify(res)
                except Exception:
                    res.update({
                        'status': 'fail'
                    })
                    current_app.logger.error(traceback.format_exc())
                    return jsonify(res)
            else:
                res.update({
                    'status': 'fail',
                    'info': 'user_not_existed'
                })
                return jsonify(res)

    else:
        res.update({
            'status': 'fail',
            'info': 'no_target_id'
        })
        return jsonify(res)