# -*- coding: utf-8 -*-
import traceback
from flask import Blueprint, render_template, current_app, request
from flask.ext.login import login_required, current_user
from nowdo import session_cm
from nowdo.controls.notice_formatted import FormattedNotice

__author__ = 'lhfu'


notice_bp = Blueprint('notice', __name__, template_folder='templates/notice')


@notice_bp.route('')
@notice_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1)

    with session_cm() as db_session:
        my_notices = FormattedNotice.get_notices_by_receiver(db_session, current_user.id, 1)
        context = {
            'my_notices': my_notices
        }
        return render_template('notice/index.html', **context)