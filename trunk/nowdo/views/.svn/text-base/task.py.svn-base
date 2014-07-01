# coding=utf-8
"""
created by SL on 14-3-19
"""
import os
import tempfile
from flask import Blueprint, render_template, redirect, url_for, flash, send_file, abort, request, jsonify
from flask.ext.login import current_user, login_required
from nowdo.controls.crowd_source_task import CrowdSourceTask, CrowdSourceTaskComment
from nowdo.controls.trends import Trends
from nowdo.controls.account import Account
from nowdo.forms.forms import CreateCommentForm, CreateTaskForm
from nowdo.utils.date_utils import date_delta
from nowdo.utils.decorators import ajax_login_required, task_admin_required
from nowdo.utils.kfile_api import kf_v1 as kf
from nowdo.utils.languages import supported_languages
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm


__author__ = 'SL'


task_bp = Blueprint('task', __name__)
supported_language_map = supported_languages()


@task_bp.route('/view/<task_id>')
def task_view(task_id):
    with session_cm() as db_session:
        context = {}
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)
        context.update({
            'task': task,
            'comment_form': CreateCommentForm(),
            'supported_languages': supported_language_map
        })
        return render_template('group/task_read.html', **context)


@task_bp.route('/<task_id>/manage')
@login_required
@task_admin_required
def manage(task_id):
    with session_cm() as db_session:
        context = {}
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)
        context.update({
            'page_header': task.name,
            'page_desc': task.description,
            'task': task,
            'supported_languages': supported_language_map
        })
        return render_template('group/task.html', **context)


@task_bp.route('/create_task', methods=['POST'])
@ajax_login_required()
def create_task():
    """
        创建主题的ajax接口
    """
    res = ajax_response()
    tar_lang_list = request.form.getlist('tar_lang')
    with session_cm() as db_session:
        form = CreateTaskForm(request.form)
        if form.validate_on_submit():
            new_task = CrowdSourceTask.create_crowd_source_task(db_session,
                                                                form.task_name.data,
                                                                form.src_lang.data,
                                                                tar_lang_list,
                                                                form.status.data,
                                                                form.tags.data,
                                                                description=form.task_description.data,
                                                                # glossary_table_id=form.glossary_table.data,
                                                                content=form.task_content.data,
                                                                max_translate_count=form.max_translate_count.data,
                                                                type=CrowdSourceTask.TASK_TYPE_TEXT)

            # if form.status.data:  # 如果是开启翻译，提交的内容一定是纯文本
            #     celery.send_task('nowdo.tasks.translate.extract_worker',
            #                      [setting.TASK_FILE_GROUP_STR, new_task.file_id, tar_lang_list])
            return jsonify(res)
        else:
            res.update({
                'status': 'fail',
                'info': u'创建主题失败'
            })
            return jsonify(res)


@task_bp.route('/task_preview', methods=['POST'])
@login_required
def task_preview():
    """
        主题预览
    """
    form = CreateTaskForm(request.form)
    context = {
        'form': form,
        'task_name': form.task_name.data,
        'task_content': form.task_content.data,
        'is_active': form.status.data
    }
    # if context['is_active']:
    #     context.update(task_entries=[entry for entry in get_unicode(context['task_content']).splitlines()])
    return render_template('group/task_preview.html', **context)


@task_bp.route('/create_img_task', methods=['POST'])
@ajax_login_required()
def create_img_task():
    """
        创建图片主题的ajax接口
    """
    res = ajax_response()
    task_name = request.form.get('task_name')
    tags = request.form.get('tags')
    src_lang = request.form.get('src_lang')
    status = request.form.get('status')
    tar_lang = request.form.get('tar_lang')
    img_list = request.form.getlist('img_list[]')
    try:
        with session_cm() as db_session:
            new_task = CrowdSourceTask.create_img_task(
                db_session,
                task_name,
                src_lang,
                [tar_lang],
                status,
                tags,
                img_list=img_list
            )

            return jsonify(res)
    except:
        res.update({
            'status': 'fail',
            'info': u'创建主题失败'
        })
        return jsonify(res)

@task_bp.route('/comments', methods=['GET'])
def comments():
    task_id = request.args.get('task_id')
    page = request.args.get('page', 1)
    res = ajax_response()
    if not task_id:
        res.update({
            'status': 'fail',
            'info': 'task_id_required'
        })
        return jsonify(res)
    with session_cm() as db_session:
        comment_pagination = CrowdSourceTaskComment.get_comments(db_session, task_id, page=page)
        creator_ids = [c.creator_id for c in comment_pagination.object_list]
        creator_list = []
        if creator_ids:
            creator_list = db_session.query(Account).filter(Account.id.in_(creator_ids)).all()
        creator_id_map = dict([(u.id, u) for u in creator_list])
        comment_dict_list = []
        for comment in comment_pagination.object_list:
            user = creator_id_map.get(comment.creator_id)
            comment_dict_list.append({
                'avatar_url': user.avatar_url(30),
                'nickname': user.nickname,
                'creator_home_url': url_for('personal.index', user_id=user.id),
                'comment_content': comment.content,
                'create_date_delta': date_delta(comment.created_date)
            })
        res.update({
            'data': comment_dict_list,
            'page': page,
            'num_pages': comment_pagination.paginator.num_pages
        })
        return jsonify(res)


@task_bp.route('/<task_id>/create_comment', methods=['POST'])
@login_required
def create_comment(task_id):
    """
    添加评论
    """
    context = {}
    form = CreateCommentForm(request.form)

    with session_cm() as db_session:
        if form.validate_on_submit():
            task = db_session.query(CrowdSourceTask).get(task_id)
            context.update({
                'comment_form': form
            })
            comment = CrowdSourceTaskComment.create_comment(db_session, task, form.content.data)
            context.update(comment=comment)
        return redirect(url_for('task.task_view', task_id=task_id))


@task_bp.route('/ajax_create_comment', methods=['POST'])
@ajax_login_required()
def ajax_create_comment():
    """
    ajax 添加评论
    """
    res = ajax_response()
    task_id = request.form.get('task_id')
    comment_content = request.form.get('comment_content')
    if not task_id or not comment_content:
        res.update({
            'status': 'fail',
            'info': u'评论内容不能为空'
        })
        return jsonify(res)
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        comment = CrowdSourceTaskComment.create_comment(db_session, task, comment_content)
        creator = comment.creator
        res.update(data={
            'avatar_url': creator.avatar_url(30),
            'nickname': creator.nickname,
            'comment_count': task.comment_count,
            'creator_home_url': url_for('personal.index', user_id=creator.id),
            'comment_content': comment.content,
            'create_date_delta': date_delta(comment.created_date)
        })
        return jsonify(res)


@task_bp.route('/<task_id>/close')
@login_required
@task_admin_required
def close_task(task_id):
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)
        task.deactivate()
        return redirect(url_for('task.manage', task_id=task_id))


@task_bp.route('/<task_id>/open')
@login_required
@task_admin_required
def open_task(task_id):
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)
        task.active()
        return redirect(url_for('task.manage', task_id=task_id))


@task_bp.route('/<task_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_task(task_id):
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)
        if not task.is_admin(current_user):
            flash(u'没有权限进行此操作', 'danger')
            return redirect(url_for('personal.published_tasks', user_id=current_user.id))

        if not task.editable:
            flash(u'任务已经被开启过，不能再进行编辑', 'info')
            return redirect(url_for('personal.published_tasks', user_id=current_user.id))

        context = {}
        if request.method == 'POST':
            tar_lang_list = request.form.getlist('tar_lang')
            form = CreateTaskForm(request.form)
            if form.validate_on_submit():
                task.update_task(task_name=form.task_name.data,
                                 task_content=form.task_content.data,
                                 status=form.status.data,
                                 src_lang=form.src_lang.data,
                                 tar_lang=tar_lang_list,
                                 tags_str=form.tags.data)

                return redirect(url_for('personal.published_tasks', user_id=current_user.id))
            else:
                flash(str(form.errors[0]), 'danger')

        context.update({
            'create_task_form': CreateTaskForm(task_name=task.name,
                                               task_content=task.task_content,
                                               src_lang=task.src_lang,
                                               tar_lang=task.tar_lang,
                                               status=task.is_translating,
                                               tags=','.join([t.tag_name for t in task.tags])),
            'task': task
        })
        return render_template('group/task_edit.html', **context)


@task_bp.route('/toggle_active_task')
@ajax_login_required()
def toggle_active_task():
    task_id = request.args.get('task_id')
    res = ajax_response()
    if task_id:
        with session_cm() as db_session:
            task = db_session.query(CrowdSourceTask).get(task_id)
            if not task:
                abort(404)
            if not task.creator_id == current_user.id:
                abort(403)

            if task.status == CrowdSourceTask.STATUS_TRANSLATING:
                task.deactivate()
            else:
                task.active()
            res.update(data=task.status == CrowdSourceTask.STATUS_TRANSLATING)
            return jsonify(res)
    else:
        res.update({
            'status': 'fail',
            'info': 'no_task_id'
        })
        return jsonify(res)


@task_bp.route('/<task_id>/delete')
@login_required
def delete_task(task_id):
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        group_id = task.group.id
        if not task:
            abort(404)
        if not task.has_translate_result():
            db_session.delete(task)
            # 删除相关动态
            Trends.remove_trends(db_session, task.id)
            db_session.commit()
        else:
            flash(u'该任务已经开始翻译，不能删除！', 'danger')
        return redirect(url_for('group.task_manage', group_id=group_id))


@task_bp.route('/translate/<task_id>')
def task_translate(task_id):
    with session_cm() as db_session:
        context = {}
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task or not task.is_translating:
            abort(404)

        context.update({
            'task': task.to_dict(with_progress=True, with_completed=False),
            'user': {
                'id': str(current_user.id),
                'is_authenticated': current_user.is_authenticated(),
                'nickname': current_user.nickname if current_user.is_authenticated() else ''
            },
            'supported_languages': supported_language_map
        })
        return render_template('group/task_translate.html', **context)


@task_bp.route('/end_translate/<task_id>/<tar_lang>')
@login_required
@task_admin_required
def end_translate(task_id, tar_lang):
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task or not tar_lang:
            abort(404)

        if tar_lang in task.completed_tar_lang_list:
            flash(u'该任务已经完成，无需重复操作！', category='info')
        else:
            result, info = task.end_translation_for_tar_lang(tar_lang)
            if not result:
                flash(info, 'danger')
        return redirect(url_for('task.manage', task_id=task.id))


@task_bp.route('/redo_translate/<task_id>/<tar_lang>')
@login_required
@task_admin_required
def redo_translate(task_id, tar_lang):
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)

        if not task:
            abort(404)

        if tar_lang not in task.completed_tar_lang_list:
            flash(u'该任务已经在翻译中！', category='info')
        else:
            task.redo_translation_for_tar_lang(tar_lang)
            task.extract_task_file()

        return redirect(url_for('task.manage', task_id=task.id))


@task_bp.route('/download/<task_id>/<tar_lang>')
@login_required
@task_admin_required
def download(task_id, tar_lang):
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)

        if not tar_lang in task.completed_tar_lang_list:
            flash(u'该任务还未完成！', category='info')
            return redirect(url_for('task.task_view', task_id=task.id))
        else:
            the_file = kf.get_file(task.file_id, tar_lang)
            temp_file, path = tempfile.mkstemp()
            os.write(temp_file, the_file.content)
            os.close(temp_file)
            return send_file(path, mimetype='application/download-me',
                             as_attachment=True, attachment_filename=the_file.lang + '-' + the_file.source)