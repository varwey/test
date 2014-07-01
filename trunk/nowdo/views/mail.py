# coding=utf-8
"""
created by SL on 14-3-7
"""
import traceback
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask.ext.login import current_user, login_required
from nowdo.controls.follows import Follow
from nowdo.controls.mail import Mail, Dialogue
from nowdo.controls.account import Account
from nowdo.forms.forms import WriteMailForm
from nowdo.utils.session import session_cm

__author__ = 'SL'


mail_bp = Blueprint('mail', __name__, template_folder='templates/mail')


@mail_bp.route('')
@mail_bp.route('/')
@login_required
def index():
    try:
        with session_cm() as db_session:
            my_dialogues = Dialogue.my_dialogues(db_session, current_user)
            context = {
                'my_dialogues': my_dialogues
            }
            return render_template('mail/index.html', **context)
    except Exception:
        current_app.logger.error(traceback.format_exc())


@mail_bp.route('/choose')
@login_required
def choose():
    """
    我关注的人列表
    """
    page = request.args.get('page', 1)
    with session_cm() as db_session:
        followed_users_pagination = Follow.followed_users(db_session, current_user, page, per_page=Follow.PER_PAGE)
        context = {
            'followed_users_pagination': followed_users_pagination
        }
        return render_template('mail/choose.html', **context)


@mail_bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    """
    写信
    """
    if request.method == 'GET':
        receiver_id = request.args.get('to')
        if not receiver_id:
            return redirect(url_for('mail.index'))
        with session_cm() as db_session:
            receiver = db_session.query(Account).get(receiver_id)

            if receiver:
                dialogue = Dialogue.get_dialogue(db_session, current_user.id, receiver.id)
                if dialogue:
                    return redirect(url_for('mail.mail_detail', dialogue_id=dialogue.id))
                context = {
                    'receiver': receiver,
                    'form': WriteMailForm(receiver_id=receiver.id)
                }
                return render_template('mail/write.html', **context)
            else:
                return redirect(url_for('mail.index'))
    else:
        form = WriteMailForm(request.form)
        context = {
            'form': form
        }
        if form.validate_on_submit():
            with session_cm() as db_session:
                dialogue = Mail.send(db_session, current_user.id, form.receiver_id.data, form.mail_content.data)
                return redirect(url_for('mail.mail_detail', dialogue_id=dialogue.id))
        return render_template('mail/write.html', **context)


@mail_bp.route('/<dialogue_id>')
@login_required
def mail_detail(dialogue_id):
    with session_cm() as db_session:
        dialogue = db_session.query(Dialogue).get(dialogue_id)
        if not dialogue:
            return redirect(url_for('mail.index'))

        dialogue.read()

        target_user = dialogue.target_user()
        sender_receiver_map = {
            current_user.id: current_user,
            target_user.id: target_user
        }
        context = {
            'sender_receiver_map': sender_receiver_map,
            'target_user': target_user,
            'mail_list': dialogue.mail_list,
            'form': WriteMailForm(receiver_id=target_user.id)
        }
        return render_template('mail/mail_detail.html', **context)