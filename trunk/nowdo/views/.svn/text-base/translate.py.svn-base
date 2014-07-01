# coding=utf-8
"""
created by SL on 14-3-13
"""
import traceback

from flask import Blueprint, request, abort, current_app, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from nowdo.controls.crowd_source_task import CrowdSourceTaskResult, CrowdSourceTask
from nowdo.controls.account import Account
from nowdo.utils.decorators import ajax_login_required, task_admin_required
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm


__author__ = 'SL'


translate_bp = Blueprint('translate', __name__)


@translate_bp.route('/fetch_entries')
def fetch_entries():
    try:
        res = ajax_response()
        task_id = request.args.get('task_id')
        tar_lang = request.args.get('tar_lang')
        
        with session_cm() as db_session:
            task = db_session.query(CrowdSourceTask).get(task_id)
            entries = task.entries()
            showed_results = task.showed_results(tar_lang)

            result_dict = dict([(str(result.entry_id), result) for result in showed_results])

            res_list = []
            for e in entries:
                result = result_dict.get(str(e.id), None)
                res_dict = {
                    'position': str(e.position),
                    'entry': {
                        'id': str(e.id),
                        'word': e.word,
                        'position': str(e.position)
                    },
                    'result': result.to_dict() if result else None
                }
                res_list.append(res_dict)
            res.update(data=res_list)
            return jsonify(res)

    except Exception:
        current_app.logger.warn(traceback.format_exc())
        abort(400)


@translate_bp.route('/fetch_glossaries')
def fetch_glossaries():
    try:
        res = ajax_response()
        if not current_user.is_authenticated():
            res.update({
                'status': 'fail',
                'info': _(u'登录后才能执行此操作')
            })
            return jsonify(res)
        task_id = request.args.get('task_id')

        with session_cm() as db_session:
            task = db_session.query(CrowdSourceTask).get(task_id)
            # glossary_tables = task.glossary_tables

            glossaries = task.glossaries

            creator_ids = [g.creator_id for g in glossaries]

            creators = db_session.query(Account).filter(Account.id.in_(creator_ids)).all()

            creator_map = dict((u.id, u.nickname) for u in creators)

            glossary_list = []
            for glossary in glossaries:
                glossary_list.append({
                    'id': str(glossary.id),
                    'source': glossary.source,
                    'target': glossary.target,
                    'creator_id': str(glossary.creator_id),
                    'creator_nickname': creator_map[glossary.creator_id],
                    'created_date': glossary.created_date.strftime('%Y-%m-%d %H:%M')
                })
            res.update(data=glossary_list)
            return jsonify(res)

    except Exception:
        current_app.logger.warn(traceback.format_exc())
        abort(400)


# @translate_bp.route('/fetch_glossary_table')
# def fetch_glossary_table():
#     try:
#         res = ajax_response()
#         if not current_user.is_authenticated():
#             res.update({
#                 'status': 'fail',
#                 'info': _(u'登录后才能执行此操作')
#             })
#             return jsonify(res)
#
#         with session_cm() as db_session:
#             glossary_tables = GlossaryTable.glossary_table_list(db_session, current_user)
#             glossary_table_list = []
#             for gt in glossary_tables:
#                 glossary_table_list.append({
#                     'id': str(gt.id),
#                     'name': gt.name
#                 })
#             res.update(data=glossary_table_list)
#             return jsonify(res)
#     except Exception:
#         current_app.logger.warn(traceback.format_exc())
#         abort(400)


@translate_bp.route('/approve', methods=['POST', 'GET'])
@login_required
@task_admin_required
def approve():
    try:
        args = request.form if request.method == 'POST' else request.args
        res = ajax_response()

        task_id = args.get('task_id')
        result_id = args.get('result_id')
        entry_id = args.get('entry_id')
        tar_lang = args.get('tar_lang')

        print task_id

        with session_cm() as db_session:
            task = db_session.query(CrowdSourceTask).get(task_id)
            if not task or not task.is_translating:
                abort(400)

            if tar_lang in task.completed_tar_lang_list:
                res.update({
                    'status': 'fail',
                    'info': _(u'该语言的翻译已经完成，不能进行该操作'),
                    'category': 'danger'
                })
                return jsonify(res)
            result = task.approve_result(entry_id, result_id, tar_lang)
            res.update(data=result.to_dict())
            db_session.commit()
            return jsonify(res)
    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(400)


@translate_bp.route('/add_trans_result', methods=['POST', 'GET'])
@ajax_login_required()
def add_trans_result():
    args = request.form if request.method == 'POST' else request.args
    entry_id = args.get('entry_id')
    entry_position = args.get('entry_position')
    task_id = args.get('task_id')
    target_text = args.get('target_text')
    tar_lang = args.get('tar_lang')

    res = ajax_response()

    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)

        used_result = db_session.query(CrowdSourceTaskResult). \
            filter(CrowdSourceTaskResult.task_id == task_id,
                   CrowdSourceTaskResult.tar_lang == tar_lang,
                   CrowdSourceTaskResult.entry_id == entry_id,
                   CrowdSourceTaskResult.used == True).first()
        if used_result:
            res.update({
                'status': 'fail',
                'info': _(u'该词条已经有翻译结果被确认')
            })
            return jsonify(res)

        result_count = db_session.query(CrowdSourceTaskResult). \
            filter(CrowdSourceTaskResult.task_id == task_id,
                   CrowdSourceTaskResult.tar_lang == tar_lang,
                   CrowdSourceTaskResult.entry_id == entry_id).count()
        if task.max_translate_count <= result_count:
            res.update({
                'status': 'fail',
                'info': _(u'翻译结果数量已达上限')
            })
            return jsonify(res)

        same_result = db_session.query(CrowdSourceTaskResult). \
            filter(CrowdSourceTaskResult.task_id == task_id,
                   CrowdSourceTaskResult.tar_lang == tar_lang,
                   CrowdSourceTaskResult.entry_id == entry_id,
                   CrowdSourceTaskResult.content == target_text,
                   CrowdSourceTaskResult.translator != current_user.email).first()
        if same_result:
            same_result.vote(delete_on_existed=False)
            res.update({
                'status': 'fail',
                'info': _(u'翻译结果已经存在，已点赞')
            })
            return jsonify(res)

        ret, result = CrowdSourceTaskResult.add_result(db_session, task_id, entry_id,
                                                       entry_position, tar_lang, target_text)
        if not ret:
            res.update({
                'status': 'fail',
                'info': result
            })
            return jsonify(res)

        res.update(data=result.to_dict())

        return jsonify(res)


@translate_bp.route('/other_results', methods=['POST', 'GET'])
@login_required
def other_results():
    res = ajax_response()
    args = request.form if request.method == 'POST' else request.args
    entry_id = args.get('entry_id')
    task_id = args.get('task_id')
    tar_lang = args.get('tar_lang')
    with_mine = args.get('with_mine') == 'true'

    with session_cm() as db_session:
        trans_results_query = db_session.query(CrowdSourceTaskResult). \
            filter(CrowdSourceTaskResult.entry_id == entry_id,
                   CrowdSourceTaskResult.task_id == task_id,
                   CrowdSourceTaskResult.tar_lang == tar_lang)

        if not with_mine:
            trans_results_query = trans_results_query.filter(CrowdSourceTaskResult.translator != current_user.email)
        trans_results_query = trans_results_query.order_by(CrowdSourceTaskResult.created_date.desc())

        trans_results = trans_results_query.all()
        translate_result_list = []
        for r in trans_results:
            result_dict = r.to_dict()
            result_dict.update({
                'voted_by_me': r.voted_by(current_user.email)
            })
            translate_result_list.append(result_dict)

        res.update(data=translate_result_list)

    return jsonify(res)


@translate_bp.route('/up_vote')
def up_vote():
    res = ajax_response()
    result_id = request.args.get('result_id')
    with session_cm() as db_session:

        trans_result = db_session.query(CrowdSourceTaskResult).get(result_id)
        if not trans_result:
            res.update({
                'info': _(u"翻译结果不存在"),
                'status': 'fail',
                'category': 'danger'
            })
            return jsonify(res)
        trans_result.vote()
        res_dict = trans_result.to_dict()
        res_dict.update(voted_by_me=trans_result.voted_by(current_user.email))
        res.update(data=res_dict)

    return jsonify(res)


# @translate_bp.route('/recommend_glossary', methods=['POST'])
# def recommend_glossary():
#     res = ajax_response()
#     task_id = request.form.get('task_id')
#     source = request.form.get('source')
#     target = request.form.get('target')
#     tar_lang = request.form.get('tar_lang')
#
#     with session_cm() as db_session:
#         task = db_session.query(CrowdSourceTask).get(task_id)
#         if not task:
#             abort(404)
#         if not current_user.is_authenticated():
#             res.update({
#                 'category': 'danger',
#                 'info': u'登录之后才能进行此操作'
#             })
#             return jsonify(res)
#
#         CheckingGlossary.create(db_session, current_user, task, source, target, tar_lang)
#         res.update({
#             'category': 'success',
#             'info': u'推荐术语成功'
#         })
#         return jsonify(res)


@translate_bp.route('/create_glossary', methods=['POST'])
def create_glossary():
    res = ajax_response()
    task_id = request.form.get('task_id')
    source = request.form.get('source')
    target = request.form.get('target')
    tar_lang = request.form.get('tar_lang')

    with session_cm() as db_session:
        task = db_session.query(CrowdSourceTask).get(task_id)
        if not task:
            abort(404)
        if not current_user.is_authenticated():
            res.update({
                'category': 'danger',
                'info': u'登录之后才能进行此操作'
            })
            return jsonify(res)

        glossary = task.create_glossary(current_user, source, target, tar_lang)
        res.update({
            'category': 'success',
            'info': u'创建术语成功',
            'data': {
                'id': str(glossary.id),
                'source': glossary.source,
                'target': glossary.target
            }
        })
        return jsonify(res)


# @translate_bp.route('/collect_glossary', methods=['POST'])
# def collect_glossary():
#     res = ajax_response()
#     glossary_table_id = request.form.get('glossary_table_id')
#     source = request.form.get('source')
#     target = request.form.get('target')
#
#     with session_cm() as db_session:
#         if not current_user.is_authenticated():
#             res.update({
#                 'category': 'danger',
#                 'info': u'登录之后才能进行此操作'
#             })
#             return jsonify(res)
#         glossary_table = db_session.query(GlossaryTable).get(glossary_table_id)
#         if not glossary_table:
#             res.update({
#                 'category': 'danger',
#                 'info': u'术语表不存在或者已经被删除'
#             })
#             return jsonify(res)
#
#         Glossary.create_glossary(db_session, source, target, glossary_table_id)
#         res.update({
#             'category': 'success',
#             'info': u'术语成功收藏到术语表：%s' % glossary_table.name
#         })
#         return jsonify(res)


@translate_bp.route('/fetch_images', methods=['POST', 'GET'])
def fetch_images():
    try:
        res = ajax_response()
        task_id = request.args.get('task_id')
        tar_lang = request.args.get('tar_lang')

        with session_cm() as db_session:
            task = db_session.query(CrowdSourceTask).get(task_id)
            entries = task.entries()
            showed_results = task.showed_results(tar_lang)

            result_dict = dict([(str(result.entry_id), result) for result in showed_results])

            res_list = []
            for e in entries:
                result = result_dict.get(str(e.id), None)
                res_dict = {
                    'position': str(e.position),
                    'entry': {
                        'id': str(e.id),
                        'word': e.word,
                        'position': str(e.position)
                    },
                    'result': result.to_dict() if result else None
                }
                res_list.append(res_dict)
            res.update(data=res_list)
            return jsonify(res)

    except Exception:
        current_app.logger.warn(traceback.format_exc())
        abort(400)