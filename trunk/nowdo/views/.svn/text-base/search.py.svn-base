# -*- coding: utf-8 -*-
import traceback
from flask import Blueprint, request, render_template, current_app, abort, jsonify
from nowdo import session_cm
from nowdo.controls.crowd_source_task import CrowdSourceTaskTagRel, CrowdSourceTask
from nowdo.controls.tag import Tag
from nowdo.utils.languages import supported_languages
from nowdo.utils.response_util import ajax_response

__author__ = 'lhfu'


search_bp = Blueprint('search', __name__, template_folder='templates/search')


@search_bp.route('/name_search')
def name_search():
    try:
        ret = ajax_response()
        search_name = request.args.get('text')
        with session_cm() as db_session:
            showed_tags = Tag.search_by_name(db_session, search_name)
            showed_tasks = CrowdSourceTask.search_by_name(db_session, search_name)

            ret.update(data={
                'showed_tasks': [showed_task.to_dict() for showed_task in showed_tasks],
                'showed_tags': [showed_tag.to_dict() for showed_tag in showed_tags],
            })

            return jsonify(ret)

    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(400)


@search_bp.route('/tag_name_search')
def tag_name_search():
    try:
        ret = ajax_response()
        tag_name = request.args.get('text')
        with session_cm() as db_session:
            showed_tags = Tag.search_by_name(db_session, tag_name)

            ret.update(data={
                'showed_tags': [showed_tag.to_dict() for showed_tag in showed_tags],
            })

            return jsonify(ret)

    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(400)


@search_bp.route('/task_name_search')
def task_name_search():
    try:
        ret = ajax_response()
        task_name = request.args.get('text')
        with session_cm() as db_session:
            showed_tasks = CrowdSourceTask.search_by_name(db_session, task_name)

            ret.update(data={
                'showed_tasks': [showed_task.to_dict() for showed_task in showed_tasks],
            })

            return jsonify(ret)

    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(400)