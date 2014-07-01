# coding=utf-8
"""
created by SL on 14-3-27
"""
from functools import wraps
from flask import Blueprint, request, abort, render_template, url_for, redirect, jsonify
from flask.ext.login import current_user, login_required
from nowdo.controls.crowd_source_task import CrowdSourceTaskTagRel
from nowdo.controls.tag import Tag
from nowdo.utils.languages import supported_languages
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm

__author__ = 'SL'

management_bp = Blueprint('management', __name__)


def super_admin_required(func):
    @wraps(func)
    def wrapper():
        if not current_user.is_super_admin():
            abort(403)
        return func()
    return wrapper


@management_bp.route('/')
@management_bp.route('/index')
@login_required
@super_admin_required
def index():
    return redirect(url_for('management.tags'))


@management_bp.route('/tags', methods=['POST', 'GET'])
@login_required
@super_admin_required
def tags():
    """
    存在主题的标签列表（标签还有可能打在了小组上）
    """
    context = {}
    page = request.args.get('page', 1)
    cur_tag_name = request.args.get('tag')
    with session_cm() as db_session:
        tag_list = Tag.task_tags(db_session)
        if cur_tag_name:
            cur_tag = Tag.get_by_name(db_session, cur_tag_name)
            task_tag_rel_pagination = CrowdSourceTaskTagRel.get_rel_list_by_tag_name(db_session, cur_tag_name, page=page)
            context.update(task_tag_rel_pagination=task_tag_rel_pagination, current_tag=cur_tag)

            for task_tag_rel in task_tag_rel_pagination.object_list:
                print task_tag_rel.task_id

        context.update({
            'tag_list': tag_list,
            'supported_languages': supported_languages()
        })

        return render_template('management/tags.html', **context)


@management_bp.route('/featured_tags', methods=['POST', 'GET'])
@super_admin_required
@login_required
def featured_tags():
    """
    所有包含精选主题的标签列表
    """
    context = {}
    page = request.args.get('page', 1)
    cur_tag_name = request.args.get('tag')
    with session_cm() as db_session:
        tag_list = Tag.task_tags(db_session, featured=True)
        if cur_tag_name:
            cur_tag = Tag.get_by_name(db_session, cur_tag_name)
            task_tag_rel_pagination = CrowdSourceTaskTagRel.get_rel_list_by_tag_name(db_session, cur_tag_name,
                                                                                     featured=True, page=page)
            context.update(task_tag_rel_pagination=task_tag_rel_pagination, current_tag=cur_tag)
        context.update({
            'tag_list': tag_list,
            'supported_languages': supported_languages()
        })

    return render_template('management/tags.html', **context)


@management_bp.route('/mark_as_featured_task', methods=['GET'])
@super_admin_required
@login_required
def mark_as_featured_task():
    task_id = request.args.get('task_id')
    tag_id = request.args.get('tag_id')
    res = ajax_response()
    with session_cm() as db_session:
        if task_id and tag_id:
            task_tag_rel = CrowdSourceTaskTagRel.get_rel(db_session, task_id, tag_id)
            task_tag_rel.is_featured = not task_tag_rel.is_featured
            db_session.commit()
            res.update(data=task_tag_rel.is_featured)
            return jsonify(res)
        else:
            res.update({
                'status': 'fail',
                'info': 'task_id and tag_id required'
            })
            return jsonify(res)
