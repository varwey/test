# coding=utf-8
"""
created by SL on 14-3-7
"""
import traceback
import uuid
from flask import Blueprint, render_template, request, abort, current_app, redirect, url_for, flash, jsonify
from flask.ext.login import current_user, login_required
from nowdo.config import setting
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.follows import Follow
from nowdo.controls.group import Group
from nowdo.controls.reg_invitation import RegInvitation
from nowdo.controls.topic import Topic
from nowdo.controls.account import Account
from nowdo.forms.forms import ProfileForm, SendRegInvitationForm
from nowdo.utils.gird_fs import new_fs
from nowdo.utils.languages import supported_languages
from nowdo.utils.paginator import InvalidPage
from nowdo.utils.session import session_cm

__author__ = 'SL'


personal_bp = Blueprint('personal', __name__, template_folder='templates/personal')
supported_language_map = supported_languages()


def base_context(db_session, user):
    if not current_user.is_authenticated():
        is_me = False
    else:
        is_me = current_user.id == user.id

    # 我关注的用户
    followed_user_pagination = Follow.followed_users(db_session, user, 1, 20)
    # 关注我的用户
    follower_pagination = Follow.followers(db_session, user, 1, 20)
    return {
        # 'page_header': '我的脑洞' if is_me else '%s 的脑洞' % user.nickname,
        'is_me': is_me,
        'owner': user,
        'followed_user_pagination': followed_user_pagination,
        'follower_pagination': follower_pagination,
        'supported_languages': supported_language_map,
    }


@personal_bp.route('')
@personal_bp.route('/<user_id>')
def index(user_id=None):
    return redirect(url_for('personal.published_tasks', user_id=user_id))
    # try:
    #     if not user_id and not current_user.is_authenticated():
    #         return redirect(url_for('account.login'))
    #     if not user_id:
    #         user_id = current_user.id
    #     with session_cm() as db_session:
    #         with account_session_cm() as account_session:
    #             user = account_session.query(Account).get(user_id)
    #             if user:
    #                 context = base_context(db_session, user)
    #                 # 我加入的小组
    #                 joined_groups_pagination = Group.joined_groups(db_session, user, 1, 5)
    #                 # 我发布的任务
    #                 published_task_pagination = CrowdSourceTask.published_tasks(db_session, user, 1, 5)
    #                 # 我参与的任务
    #                 participated_task_pagination = CrowdSourceTask.participated_tasks(db_session, user, 1, 5)
    #                 # 我喜欢的任务
    #                 liked_task_pagination = CrowdSourceTask.liked_tasks(db_session, user, 1, 5)
    #                 # # 我发布的话题
    #                 # published_topic_pagination = Topic.published_topics(db_session, user, 1, 5)
    #                 # # 我回复的话题
    #                 # commented_topic_pagination = Topic.commented_topics(db_session, user, 1, 5)
    #
    #                 context.update({
    #                     'joined_groups': joined_groups_pagination,
    #                     'published_task_pagination': published_task_pagination,
    #                     'participated_task_pagination': participated_task_pagination,
    #                     'liked_task_pagination': liked_task_pagination
    #                     # 'published_topic_pagination': published_topic_pagination,
    #                     # 'commented_topic_pagination': commented_topic_pagination
    #                 })
    #                 return render_template('personal/index.html', **context)
    #             else:
    #                 abort(404)
    # except InvalidPage:
    #     current_app.logger.error(traceback.format_exc())
    #     abort(404)


@personal_bp.route('/<user_id>/joined_groups')
def joined_groups(user_id):
    try:
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            user = db_session.query(Account).get(user_id)
            if user:
                context = base_context(db_session, user)
                joined_groups_pagination = Group.joined_groups(db_session, user, page)
                context.update({
                    'joined_groups_pagination': joined_groups_pagination
                })
                return render_template('personal/joined_groups.html', **context)
            else:
                abort(404)
    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)


@personal_bp.route('/<user_id>/participated_tasks')
def participated_tasks(user_id):
    try:
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            user = db_session.query(Account).get(user_id)
            if user:
                context = base_context(db_session, user)
                participated_task_pagination = CrowdSourceTask.participated_tasks(db_session, user, page)
                context.update({
                    'participated_task_pagination': participated_task_pagination
                })
                return render_template('personal/participated_tasks.html', **context)
            else:
                abort(404)
    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)


@personal_bp.route('/<user_id>/published_tasks')
def published_tasks(user_id):
    try:
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            user = db_session.query(Account).get(user_id)
            if user:
                context = base_context(db_session, user)
                published_task_pagination = CrowdSourceTask.published_tasks(db_session, user, page)
                context.update({
                    'published_task_pagination': published_task_pagination
                })
                return render_template('personal/published_tasks.html', **context)
            else:
                abort(404)
    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)


@personal_bp.route('/<user_id>/liked_tasks')
def liked_tasks(user_id):
    try:
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            user = db_session.query(Account).get(user_id)
            if user:
                context = base_context(db_session, user)
                liked_task_pagination = CrowdSourceTask.liked_tasks(db_session, user, page)
                context.update({
                    'liked_task_pagination': liked_task_pagination
                })
                return render_template('personal/like_tasks.html', **context)
            else:
                abort(404)
    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)


@personal_bp.route('/<user_id>/followed_users')
def followed_users(user_id):
    try:
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            user = db_session.query(Account).get(user_id)
            if user:
                context = base_context(db_session, user)
                followed_users_pagination = Follow.followed_users(db_session, user, page)
                context.update({
                    'followed_users_pagination': followed_users_pagination
                })
                return render_template('personal/followed_users.html', **context)
            else:
                abort(404)
    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)


@personal_bp.route('/<user_id>/published_topics')
def published_topics(user_id):
    try:
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            user = db_session.query(Account).get(user_id)
            if user:
                context = base_context(db_session, user)
                published_topic_pagination = Topic.published_topics(db_session, user, page)
                context.update({
                    'published_topic_pagination': published_topic_pagination
                })
                return render_template('personal/published_topics.html', **context)
            else:
                abort(404)
    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)


@personal_bp.route('/<user_id>/commented_topics')
def commented_topics(user_id):
    try:
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            user = db_session.query(Account).get(user_id)
            if user:
                context = base_context(db_session, user)
                commented_topic_pagination = Topic.commented_topics(db_session, user, page)
                context.update({
                    'commented_topic_pagination': commented_topic_pagination
                })
                return render_template('personal/commented_topics.html', **context)
            else:
                abort(404)
    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)


@personal_bp.route('/avatar_upload', methods=['POST'])
@login_required
def avatar_upload():
    res = {
        "code": 200,
        "msg": u"上传成功"
    }
    with session_cm() as account_session:
        if not current_user.session:
            account_session.add(current_user)

        file_name = '/'.join([setting.AVATAR_FILE_GROUP_STR, str(uuid.uuid4()) + '.jpg'])
        avatar_id = new_fs.save_file(file_name, request.stream.read(), content_type='image/jpeg')
        current_user.update_property('avatar_id', avatar_id)
        current_user.session.commit()

        res.update(pic=url_for('frontend.get_file', file_id=avatar_id))
        return jsonify(res)


@personal_bp.route('/my_profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    form = None
    if request.method == 'GET':
        form = ProfileForm(obj=current_user)

    if request.method == 'POST':
        form = ProfileForm(request.form)
        if form.validate_on_submit():
            with session_cm() as account_session:
                current_user.display_name = form.display_name.data
                if not current_user.session:
                    account_session.add(current_user)
                current_user.session.commit()
                flash(message=u'账号信息更新成功', category='success')

    context = {
        'form': form
    }

    return render_template('personal/profile.html', **context)


@personal_bp.route('/my_avatar', methods=['GET', 'POST'])
@login_required
def my_avatar():
    return render_template('personal/avatar.html')


@personal_bp.route('/<user_id>/reg_invitation', methods=['GET', 'POST'])
@login_required
def reg_invitation(user_id):
    try:
        if request.method == 'GET':
            page = request.args.get('page', 1)
            with session_cm() as db_session:
                user = db_session.query(Account).get(user_id)
                if user:
                    context = base_context(db_session, user)
                    reg_invitation_pagination = RegInvitation.get_invitees(db_session, user_id, page)
                    context.update({
                        'reg_invitation_pagination': reg_invitation_pagination,
                        'form': SendRegInvitationForm()
                    })
                    return render_template('personal/register_invitation.html', **context)
                else:
                    abort(404)
        else:
            form = SendRegInvitationForm(request.form)
            if form.validate_on_submit():
                with session_cm() as db_session:
                    # with account_session_cm() as account_session:
                        # new_user = Account()
                        # new_user.email = form.email.data  # .split('@')[0]
                        # new_user.name = form.email.data  # .split('@')[0]
                        # new_user.display_name = form.email.data
                        # new_passwd = generate_passwd()
                        # new_user.set_password(new_passwd)
                        # # 邀请的用户默认激活
                        # new_user.active = True
                        # account_session.add(new_user)
                        # account_session.commit()
                        # official_account = account_session.query(Account).filter(Account.email == setting.OFFICIAL_ACCOUNT).first()
                        # if official_account:
                        #     Follow.follow(new_user, target_user=official_account)
                        # 发送邀请邮件
                    Account.send_reg_invitation_mail(host_url=request.host_url, name=form.email.data, email=form.email.data)

                    reg_invitation = RegInvitation.create(db_session, user_id, form.email.data)

                    return redirect(url_for('personal.reg_invitation', user_id=user_id))
            else:
                page = request.form.get('page', 1)
                with session_cm() as db_session:
                    user = db_session.query(Account).get(user_id)
                    if user:
                        context = base_context(db_session, user)
                        reg_invitation_pagination = RegInvitation.get_invitees(db_session, user_id, page)
                        context.update({
                            'reg_invitation_pagination': reg_invitation_pagination,
                            'form': form
                        })
                        return render_template('personal/register_invitation.html', **context)
                    else:
                        abort(404)

    except InvalidPage:
        current_app.logger.error(traceback.format_exc())
        abort(404)
