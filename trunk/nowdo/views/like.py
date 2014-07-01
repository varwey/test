# coding=utf-8
"""
created by SL on 14-3-27
"""
import traceback
from flask import Blueprint, request, current_app, jsonify
from flask.ext.login import current_user
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.like import LikeRel
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm

__author__ = 'SL'

like_bp = Blueprint('like', __name__)


@like_bp.route('/like_task')
def like():
    target_id = request.args.get('target_id')
    res = ajax_response()

    if not current_user.is_authenticated():
        res.update({
            'status': 'fail',
            'info': 'not_login'
        })
        return jsonify(res)

    if target_id:
        with session_cm() as db_session:
            task = db_session.query(CrowdSourceTask).get(target_id)
            if task:
                try:
                    like_res = LikeRel.toggle_like(db_session, current_user, task)
                    res.update(data={
                        'ret': like_res,
                        'like_count': task.like_count
                    })
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
                    'info': 'task_not_existed'
                })
                return jsonify(res)

    else:
        res.update({
            'status': 'fail',
            'info': 'no_target_id'
        })
        return jsonify(res)
