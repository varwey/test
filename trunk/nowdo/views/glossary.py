# coding=utf-8
"""
created by SL on 14-4-4
"""
from flask import request, Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.glossary import Glossary
from nowdo.forms.forms import GlossaryForm
from nowdo.utils.languages import supported_languages
from nowdo.utils.session import session_cm


__author__ = 'SL'

glossary_bp = Blueprint('glossary', __name__)

base_context = {
    'page_header': u'我的术语'
}


@glossary_bp.route('/')
@login_required
def index():
    context = base_context
    page = request.args.get('page', 1)
    with session_cm() as db_session:
        task_pagination = CrowdSourceTask.tasks_with_my_glossary(db_session, current_user, page=page)

        context.update({
            'task_pagination': task_pagination
        })

    return render_template('glossary/index.html', **context)


@glossary_bp.route('/<task_id>')
@login_required
def glossary_list(task_id):
    context = base_context
    page = request.args.get('page', 1)
    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)
        glossaries = Glossary.my_glossaries(db_session, task, user=current_user, page=page)
        context.update({
            'task': task,
            'glossaries': glossaries,
            'supported_languages': supported_languages()
        })

    return render_template('glossary/glossary_list.html', **context)


# @glossary_bp.route('/table/<glossary_table_id>')
# @login_required
# def glossary_table(glossary_table_id):
#     with session_cm() as db_session:
#         g_table = db_session.query(GlossaryTable).options(joinedload(GlossaryTable.glossaries)).get(glossary_table_id)
#         if not g_table:
#             abort(404)
#
#         context = {
#             'page_header': '术语表：%s' % g_table.name,
#             'supported_languages': supported_languages(with_short=True),
#             'glossary_table': g_table
#         }
#
#     return render_template('glossary/glossary_table.html', **context)


# @glossary_bp.route('/table/<glossary_table_id>/create', methods=['GET', 'POST'])
# @login_required
# def create_glossary(glossary_table_id):
#     with session_cm() as db_session:
#         form = GlossaryForm(request.form)
#
#         if request.method == 'POST' and form.validate_on_submit():
#             Glossary.create_glossary(db_session, form.source.data, form.target.data, glossary_table_id)
#             return redirect(url_for('glossary.glossary_table', glossary_table_id=glossary_table_id))
#         else:
#             g_table = db_session.query(GlossaryTable) \
#                 .options(joinedload(GlossaryTable.glossaries)) \
#                 .get(glossary_table_id)
#             if not g_table:
#                 abort(404)
#
#             context = {
#                 'page_header': '术语表 %s 创建术语' % g_table.name,
#                 'glossary_table': g_table,
#                 'form': form
#             }
#             return render_template('glossary/create_glossary.html', **context)


@glossary_bp.route('/<glossary_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_glossary(glossary_id):
    with session_cm() as db_session:
        glossary = db_session.query(Glossary).get(glossary_id)
        db_session.delete(glossary)
        db_session.commit()
        return redirect(url_for('glossary.glossary_table', glossary_table_id=glossary.glossary_table_id))


@glossary_bp.route('/<glossary_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_glossary(glossary_id):
    with session_cm() as db_session:
        glossary = db_session.query(Glossary).get(glossary_id)
        if not glossary:
            abort(404)
        if request.method == 'POST':
            form = GlossaryForm(request.form)
            if form.validate_on_submit():
                glossary.edit(form.source.data, form.target.data)
            return redirect(url_for('glossary.glossary_table', glossary_table_id=glossary.glossary_table_id))
        else:
            form = GlossaryForm(obj=glossary)
            context = {
                'page_header': '编辑术语',
                'glossary': glossary,
                'form': form
            }
            return render_template('glossary/edit_glossary.html', **context)


# @glossary_bp.route('/checking')
# @login_required
# def checking():
#     context = base_context
#     page = request.args.get('page', 1)
#     with session_cm() as db_session:
#         glossary_tables = GlossaryTable.glossary_table_list(db_session, current_user)
#         checking_glossary_pagination = CheckingGlossary.checking_glossaries(db_session, current_user, page=page)
#         context.update({
#             'checking_glossary_pagination': checking_glossary_pagination,
#             'glossary_tables': glossary_tables
#         })
#     return render_template('glossary/checking.html', **context)


# @glossary_bp.route('/checking/<glossary_id>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_checking_glossary(glossary_id):
#     with session_cm() as db_session:
#         glossary = db_session.query(CheckingGlossary).get(glossary_id)
#         if not glossary:
#             abort(404)
#
#         glossary_tables = db_session.query(GlossaryTable)\
#             .filter(GlossaryTable.source_language == glossary.source_language,
#                     GlossaryTable.target_language == glossary.target_language).all()
#
#         glossary_table_choices = [(str(gt.id), gt.name) for gt in glossary_tables]
#         if request.method == 'POST':
#             form = CheckingGlossaryForm(request.form)
#             form.glossary_table.choices = glossary_table_choices or [('', '请先建立一个术语表')]
#             if form.validate_on_submit():
#                 glossary.edit_and_pass_check(form.source.data, form.target.data, form.glossary_table.data)
#                 return redirect(url_for('glossary.checking'))
#         else:
#             form = CheckingGlossaryForm(obj=glossary)
#             form.glossary_table.choices = glossary_table_choices or [('', '请先建立一个术语表')]
#
#         context = {
#             'page_header': '编辑审核中的术语',
#             'supported_languages': supported_languages(with_short=True),
#             'glossary': glossary,
#             'form': form
#         }
#         return render_template('glossary/edit_checking_glossary.html', **context)


# @glossary_bp.route('/pass_glossary', methods=['POST'])
# def pass_glossary():
#     glossary_ids = request.form.getlist('glossary_id')
#     glossary_table_id = request.form.get('glossary_table_id')
#
#     with session_cm() as db_session:
#         g_table = db_session.query(GlossaryTable).get(glossary_table_id)
#         if not glossary_ids:
#             flash(u'请选择术语', 'danger')
#         elif not g_table:
#             flash(u'术语表不存在或者已经被删除', 'danger')
#         else:
#             cannot_be_passed_glossaries = CheckingGlossary.patch_pass_check(db_session, glossary_ids, g_table)
#             if len(cannot_be_passed_glossaries) > 0:
#                 flash(u'部分术语的语言与您选择的术语表语言不一致', 'info')
#         return redirect(url_for('glossary.checking'))


# @glossary_bp.route('/create_glossary_table', methods=['GET', 'POST'])
# def create_glossary_table():
#     form = GlossaryTableForm(request.form)
#     context = {
#         'form': form,
#         'page_header': u'新建术语表'
#     }
#
#     if request.method == 'POST' and form.validate_on_submit():
#         with session_cm() as db_session:
#             GlossaryTable.create_glossary_table(db_session,
#                                                 name=form.name.data,
#                                                 source_language=form.source_language.data,
#                                                 target_language=form.target_language.data)
#             return redirect(url_for('glossary.index'))
#     return render_template('glossary/create_glossary_table.html', **context)