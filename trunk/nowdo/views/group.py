# coding=utf-8
"""
created by SL on 14-3-6
"""
import traceback
import uuid
from flask import request, Blueprint, render_template, redirect, url_for, flash, current_app, abort, jsonify
from flask.ext.login import login_required, current_user
from nowdo.config import setting
from nowdo.controls.group import Group
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.topic import Topic, TopicComment
from nowdo.forms.forms import CreateCommentForm, CreateGroupForm, CreateTaskForm, \
    CreateTopicForm, EditGroupForm
from nowdo.utils.decorators import ajax_login_required, group_admin_required
from nowdo.utils.gird_fs import new_fs
from nowdo.utils.languages import supported_languages
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm
from nowdo.config.celeryconfig import celery


__author__ = 'SL'


group_bp = Blueprint('group', __name__)
supported_language_map = supported_languages()


@group_bp.route('')
def index():
    return 'Group Index'


@group_bp.route('/view/<group_id>')
def group_home(group_id=None):
    if group_id:
        with session_cm() as db_session:
            context = {}
            group = db_session.query(Group).get(group_id)
            if not group:
                abort(404)
            context.update({
                'group': group,
                # 'tasks': group.available_tasks(),
                'tasks': group.tasks,
                # 'topics': group.topics,
                'members': group.member_list(),
                # 'page_header': group.group_name,
                'supported_languages': supported_language_map
                # 'page_desc': group.group_description
            })
            return render_template('group/index.html', **context)


@group_bp.route('/topic/<topic_id>')
def topic_view(topic_id):
    if topic_id:
        with session_cm() as db_session:
            context = {}
            topic = db_session.query(Topic).get(topic_id)
            if not topic:
                abort(404)
            context.update({
                'topic': topic,
                'comment_form': CreateCommentForm()
            })
            return render_template('group/topic.html', **context)


@group_bp.route('/comment/<comment_id>')
def comment_view(comment_id):
    if comment_id:
        with session_cm() as db_session:
            comment = db_session.query(TopicComment).get(comment_id)
            if not comment:
                abort(404)

            return redirect(url_for('group.topic_view', topic_id=comment.topic.id) + '#comment' + str(comment.id))


@group_bp.route('/create_group', methods=['POST', 'GET'])
@login_required
def create_group():
    context = {}
    if request.method == 'POST':
        form = CreateGroupForm(request.form)
        if form.validate_on_submit():
            Group.create_group(form.group_name.data, form.group_description.data, form.group_tags.data)
            return redirect(url_for('frontend.index'))
    else:
        form = CreateGroupForm()

    context.update({
        'form': form,
        'page_header': u'创建小组'
    })
    return render_template('group/create_group.html', **context)


@group_bp.route('/<group_id>/create_task', methods=['POST', 'GET'])
@login_required
def create_task(group_id):
    tar_langs = request.form.getlist('tar_lang')

    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        if not group:
            abort(404)

        if not group.is_member(current_user):
            flash(u'加入小组后才能发布新主题', 'info')
            return redirect(url_for('group.group_home', group_id=group_id))

        form = CreateTaskForm(request.form)

        context = {
            'group': group,
            'form': form
        }
        # glossary_table = GlossaryTable.glossary_table_list(db_session, current_user)
        # glossary_table_choices = [('', u'选择一个术语表')]
        # glossary_table_choices.extend([(str(g_table.id), g_table.name) for g_table in glossary_table])
        # form.glossary_table.choices = glossary_table_choices

        if request.method == 'POST':
            if form.validate_on_submit():
                task_file = None
                if form.input_mode.data == 'file':
                    task_file = request.files.get('task_file')

                new_task = CrowdSourceTask.create_crowd_source_task(db_session,
                                                                    form.task_name.data,
                                                                    form.src_lang.data,
                                                                    tar_langs,
                                                                    form.status.data,
                                                                    form.tags.data,
                                                                    description=form.task_description.data,
                                                                    content=form.task_content.data,
                                                                    uploaded_file=task_file,
                                                                    # glossary_table_id=form.glossary_table.data,
                                                                    group=group,
                                                                    max_translate_count=form.max_translate_count.data)
                # if form.status.data:
                #     celery.send_task('nowdo.tasks.translate.extract_worker', [group.id, new_task.file_id, tar_langs])

                return redirect(url_for('group.group_home', group_id=group_id))
        else:
            context.update({
                'form': CreateTaskForm(input_mode='text', tar_lang='cn', src_lang='en')
            })
        return render_template('group/create_task.html', **context)


@group_bp.route('/<group_id>/create_topic', methods=['POST', 'GET'])
@login_required
def create_topic(group_id):
    """
    创建话题
    """
    context = {}
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        if request.method == 'POST':
            form = CreateTopicForm(request.form)
            if form.validate_on_submit():

                    topic = Topic.create_topic(db_session, group, form.title.data, form.content.data)
                    return redirect(url_for('group.topic_view', topic_id=topic.id))
        else:
            if not group.is_member(current_user):
                flash(u'只有小组成员才能发起新的话题', category='info')
                return redirect(url_for('group.group_home', group_id=group_id))

            form = CreateTopicForm()

        context.update({
            'form': form,
            'group': group,
            'page_header': u'%s 创建话题' % group.group_name
        })
        return render_template('group/create_topic.html', **context)


@group_bp.route('/topic/<topic_id>/create_comment', methods=['POST'])
@login_required
def create_comment(topic_id):
    """
    添加评论
    """
    context = {}
    form = CreateCommentForm(request.form)

    with session_cm() as db_session:
        if form.validate_on_submit():
            topic = db_session.query(Topic).get(topic_id)
            context.update({
                'comment_form': form
            })
            comment = TopicComment.create_comment(db_session, topic, form.content.data)
            context.update(comment=comment)
        return redirect(url_for('group.topic_view', topic_id=topic_id))


@group_bp.route('/<group_id>/join')
@login_required
def join_group(group_id):
    """
    加入小组
    """
    res = ajax_response()
    try:
        with session_cm() as db_session:
            group = db_session.query(Group).get(group_id)
            group.add_member(current_user)
            return redirect(url_for('group.group_home', group_id=group_id))
    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(400)


@group_bp.route('/<group_id>/quit')
@login_required
def quit_group(group_id):
    """
    退出小组
    """
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        if not group.creator_id == current_user.id:
            group.remove_member(current_user)
        else:
            flash(u'小组的创建者不能退出小组', 'info')
        return redirect(url_for('group.group_home', group_id=group_id))


@group_bp.route('/<group_id>/toggle_join')
@ajax_login_required()
def toggle_join(group_id):
    """
    ajax 加入、退出小组
    """
    res = ajax_response()
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        if not group.creator_id == current_user.id:
            ret = group.toggle_join(current_user)
            res.update(data=(ret == 'joined'))
            return jsonify(res)
        else:
            res.update({
                'status': 'fail',
                'info': u'创建者不能退出小组'
            })
            return jsonify(res)


@group_bp.route('/<group_id>/common_setting', methods=['GET', 'POST'])
@login_required
@group_admin_required
def common_setting(group_id):
    """
    修改小组基本信息
    """
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        context = {
            'group': group
        }
        if request.method == "GET":
            tags = ','.join([t.tag_name for t in group.tags])
            context.update({
                'form': EditGroupForm(obj=group, group_tags=tags)
            })
            return render_template('group/common_setting.html', **context)
        if request.method == "POST":
            form = EditGroupForm(request.form)
            context.update({
                'form': form
            })
            if form.validate_on_submit():
                group.update_common_info(group_name=form.group_name.data,
                                         group_description=form.group_description.data,
                                         group_tags_str=form.group_tags.data)
                return redirect(url_for('group.group_home', group_id=group.id))
            else:
                return render_template('group/common_setting.html', **context)


@group_bp.route('/<group_id>/members', methods=['POST', 'GET'])
@login_required
@group_admin_required
def members(group_id):
    """
    小组成员管理
    """
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        context = {
            'group': group,
            'members': group.member_list()
        }
        return render_template('group/members.html', **context)


@group_bp.route('/<group_id>/task_manage', methods=['POST', 'GET'])
@login_required
@group_admin_required
def task_manage(group_id):
    """
    任务管理
    """
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        context = {
            'group': group,
            'tasks': group.tasks
        }
        return render_template('group/task_manage.html', **context)


@group_bp.route('/<group_id>/avatar_manage', methods=['POST', 'GET'])
@login_required
@group_admin_required
def avatar_manage(group_id):
    """
    头像管理
    """
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        context = {
            'group': group,
            'tasks': group.tasks
        }
        return render_template('group/avatar.html', **context)


@group_bp.route('/<group_id>/add_manager/<user_id>', methods=['POST', 'GET'])
@login_required
@group_admin_required
def add_manager(group_id, user_id):
    """
    晋升小组成员为管理员
    """
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        if not group.add_manager(user_id):
            flash(u'操作失败', 'danger')
    return redirect(url_for('group.members', group_id=group_id))


@group_bp.route('/<group_id>/remove_manager/<user_id>', methods=['POST', 'GET'])
@login_required
@group_admin_required
def remove_manager(group_id, user_id):
    """
    取消管理员资格
    """
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        if not group.remove_manager(user_id):
            flash(u'操作失败', 'danger')
    return redirect(url_for('group.members', group_id=group_id))


@group_bp.route('/<group_id>/avatar_upload', methods=['POST'])
@login_required
@group_admin_required
def avatar_upload(group_id):
    res = {
        "code": 200,
        "msg": u"上传成功"
    }
    with session_cm() as db_session:
        group = db_session.query(Group).get(group_id)
        if group:
            file_name = '/'.join([setting.AVATAR_FILE_GROUP_STR, str(uuid.uuid4()) + '.jpg'])
            avatar_id = new_fs.save_file(file_name, request.stream.read(), content_type='image/jpeg')
            group.set_property('avatar_id', avatar_id)
            db_session.commit()
            res.update(pic=url_for('frontend.get_file', file_id=avatar_id))
            return jsonify(res)