# coding=utf-8
from operator import or_
import re
import traceback
import uuid
from flask import Blueprint, render_template, request, current_app, abort, url_for, make_response, jsonify, redirect
from flask.ext.login import current_user, login_required
from nowdo.config import setting
from nowdo.controls.crowd_source_task import CrowdSourceTask, CrowdSourceTaskTagRel
from nowdo.controls.follows import Follow
from nowdo.controls.group import Group
from nowdo.controls.tag import Tag
from nowdo.controls.topic import Topic
from nowdo.controls.trends import Trends
from nowdo.forms.forms import CreateTaskForm
from nowdo.utils.formatted_trends import FormattedTrends
from nowdo.utils.gird_fs import new_fs
from nowdo.utils.languages import supported_languages
from nowdo.utils.response_util import ajax_response
from nowdo.utils.session import session_cm

__author__ = 'SL'

frontend_bp = Blueprint('frontend', __name__, template_folder="templates/frontend")


@frontend_bp.route('/nowdo_languages')
def nowdo_languages():
    try:
        res = ajax_response()
        print supported_languages()
        res.update(data = {
            'supported_languages': supported_languages()
        })
        return jsonify(res)
    except:
        print(traceback.format_exc())
        abort(400)


@frontend_bp.route('/')
def frontend():
    if current_user.is_authenticated():
        return redirect(url_for('frontend.index'))

    with session_cm() as db_session:
        tag_tuple = (u'文学', u'动漫', u'电影', u'旅游', u'科技', u'时尚')

        frontend_page_data_map = {}

        for tag in tag_tuple:
            frontend_page_data_map[tag] = {
                'tasks': CrowdSourceTask.featured_tasks(db_session, tag_name=tag, page=1, per_page=6).object_list
                # 'topics': Topic.hot_topics(db_session, tag=tag, page=1, per_page=15).object_list
            }

        context = {
            'frontend_page_data_map': frontend_page_data_map,
            'supported_languages': supported_languages()
        }
    return render_template('frontend/frontend.html', **context)


@frontend_bp.route('/frontend')
def frontend_login_ed():
    with session_cm() as db_session:
        tag_tuple = (u'文学', u'动漫', u'电影', u'旅游', u'科技', u'时尚')

        frontend_page_data_map = {}

        for tag in tag_tuple:
            frontend_page_data_map[tag] = {
                'tasks': CrowdSourceTask.featured_tasks(db_session, tag_name=tag, page=1, per_page=6).object_list
            }

        context = {
            'frontend_page_data_map': frontend_page_data_map,
            'supported_languages': supported_languages()
        }
    return render_template('frontend/frontend.html', **context)


@frontend_bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1)

    with session_cm() as db_session:
        # 我的主题（趋势）
        # 我喜欢的主题（趋势）
        # 我关注的人的主题（趋势）
        # 我关注的人喜欢的主题（趋势）
        followed_user_ids = Follow.followed_user_ids(db_session, current_user)
        followed_user_ids.append(current_user.id)
        trends_pagination = Trends.get_trends_list(db_session, user_ids=followed_user_ids, page=page)
        trends_list = FormattedTrends.get_formatted_trends_list(trends_pagination.object_list)

        joined_groups = Group.joined_groups(db_session, current_user, 1, 10).object_list
        followed_users = Follow.followed_users(db_session, current_user, 1, 10).object_list

        # 热门小组
        hot_groups = Group.hot_groups(db_session, page=1, per_page=10).object_list
        # 活跃用户
        passionate_users_pagination, user_id_trends_count_map = Trends.passionate_users(page=1, per_page=10)
        # 精选文章
        featured_tasks = CrowdSourceTask.featured_tasks(db_session, page=1, per_page=10).object_list

        context = {
            'hot_groups': hot_groups,
            'create_task_form': CreateTaskForm(src_lang='cn', tar_lang='en', input_mode='text', status=True),
            'trends_list': trends_list,
            'trends_pagination': trends_pagination,
            'joined_groups': joined_groups,
            'followed_users': followed_users,
            'passionate_users_pagination': passionate_users_pagination,
            'user_id_trends_count_map': user_id_trends_count_map,
            'featured_tasks': featured_tasks,
            'supported_languages': supported_languages()
        }
        return render_template('frontend/index.html', **context)


@frontend_bp.route('/tag')
def tag_view():
    try:
        tag_name = request.args.get('tag')
        page = request.args.get('page', 1)
        with session_cm() as db_session:
            context = {}
            all_tags = Tag.task_tags(db_session)
            task_tag_rel_pagination = CrowdSourceTaskTagRel.get_rel_list_by_tag_name(db_session, tag_name, page=page)
            context.update({
                'all_tags': all_tags,
                'task_tag_rel_pagination': task_tag_rel_pagination,
                'supported_languages': supported_languages(),
                'current_tag_name': tag_name
            })
            return render_template('frontend/tag.html', **context)
    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(400)


@frontend_bp.route('/explore')
def explore():
    with session_cm() as db_session:
        # 标签
        tag_tuple = (u'文学', u'动漫', u'电影', u'旅游', u'科技', u'时尚')
        # recommend_tag_task_map = {}
        # for tag in tag_tuple:
        #     recommend_tag_task_map[tag] = \
        #         CrowdSourceTask.featured_tasks(db_session, tag_name=tag, page=1, per_page=1).object_list
        # hot_tags = Tag.hot_tags(db_session, 50)

        # 主题
        task_tags = Tag.task_tags(db_session, page=1, per_page=4)

        # 小组
        hot_groups_pagination = Group.explore_hot_groups(db_session, page=1, per_page=4)

        context = {
            'one_column': True,
            'tag_tuple': tag_tuple,
            # 'hot_tags': hot_tags,
            # 'recommend_tag_task_map': recommend_tag_task_map,
            'task_tags': task_tags,
            'hot_groups_pagination': hot_groups_pagination,
            'supported_languages': supported_languages()
        }
    return render_template('frontend/explore.html', **context)


@frontend_bp.route('/explore/tags')
def explore_tags():
    with session_cm() as db_session:

        tag_tuple = (u'文学', u'动漫', u'电影', u'旅游', u'科技', u'时尚')

        # recommend_tag_task_map = {}
        #
        # for tag in tag_tuple:
        #     recommend_tag_task_map[tag] = \
        #         CrowdSourceTask.featured_tasks(db_session, tag_name=tag, page=1, per_page=1).object_list

        hot_tags = Tag.hot_tags(db_session, 50)

        context = {
            'one_column': True,
            'hot_tags': hot_tags,
            'tag_tuple': tag_tuple,
            # 'recommend_tag_task_map': recommend_tag_task_map,
            'supported_languages': supported_languages()
        }
    return render_template('frontend/explore_tags.html', **context)


@frontend_bp.route('/explore/tasks')
def explore_tasks():
    with session_cm() as db_session:
        page = request.args.get('page', 1)
        task_tags = Tag.task_tags(db_session, page=page)
        context = {
            'one_column': True,
            'task_tags': task_tags
        }
    return render_template('frontend/explore_tasks.html', **context)


@frontend_bp.route('/explore/groups')
def explore_groups():
    with session_cm() as db_session:
        tag = request.args.get('tag')
        hot_groups_pagination = Group.explore_hot_groups(db_session, tag, page=1, per_page=20)

        context = {
            'one_column': True,
            'cur_tag': tag,
            'hot_groups_pagination': hot_groups_pagination
        }
    return render_template('frontend/explore_groups.html', **context)


@frontend_bp.route('/featured')
def featured():
    with session_cm() as db_session:
        page = request.args.get('page', 1)
        tag_name = request.args.get('tag')
        tag_list = Tag.task_tags(db_session, featured=True)
        task_tag_rel_pagination = CrowdSourceTaskTagRel.get_rel_list_by_tag_name(db_session, tag_name=tag_name,
                                                                                 featured=True, page=page)

        hot_groups = Group.explore_hot_groups(db_session, page=1, per_page=5).object_list
        latest_groups = Group.latest_groups(db_session, page=1, per_page=5, with_current_user_joined=False).object_list
        passionate_users_pagination, user_id_trends_count_map = Trends.passionate_users(page=1, per_page=10)
        context = {
            'current_tag_name': tag_name,
            'featured_tags': tag_list,
            'task_tag_rel_pagination': task_tag_rel_pagination,
            'latest_groups': latest_groups,
            'hot_groups': hot_groups,
            'passionate_users_pagination': passionate_users_pagination,
            'user_id_trends_count_map': user_id_trends_count_map,
            'supported_languages': supported_languages()
        }
    return render_template('frontend/featured.html', **context)


@frontend_bp.route('/search', methods=['POST', 'GET'])
def search():
    try:
        with session_cm() as db_session:
            args = request.args if request.method == 'GET' else request.form
            page = args.get('page', 1)
            key_word = args.get('keyword', None)
            context = {}
            if key_word:
                search_param = '%' + key_word + '%'
                # 搜索小组
                groups_ids = db_session.query(Group.id)\
                    .filter(or_(Group.group_name.like(search_param),
                                Group.group_description.like(search_param))).all()
                # 搜索话题
                topic_ids = db_session.query(Topic.id)\
                    .filter(or_(Topic.title.like(search_param),
                                Topic.content.like(search_param))).all()
                # 搜索任务
                task_ids = db_session.query(CrowdSourceTask.id)\
                    .filter(or_(CrowdSourceTask.name.like(search_param),
                            CrowdSourceTask.description.like(search_param))).all()
                trends_target_ids = []
                trends_target_ids.extend(groups_ids)
                trends_target_ids.extend(topic_ids)
                trends_target_ids.extend(task_ids)
                trends_target_ids = map(lambda x: x[0], trends_target_ids)

                trends_pagination = Trends.get_trends_list_from_target_ids(trends_target_ids,
                                                                           page=page, per_page=Trends.PER_PAGE)
                object_list = trends_pagination.object_list if trends_pagination else []
                formatted_trends_list = FormattedTrends.get_formatted_trends_list(object_list)

                context.update({
                    'trends_list': formatted_trends_list,
                    'trends_pagination': trends_pagination,
                    'keyword': key_word,
                    'supported_languages': supported_languages()
                })
            return render_template('frontend/search.html', **context)
    except Exception:
        current_app.logger.error(traceback.format_exc())
        abort(400)


@frontend_bp.route('/file/save', methods=['POST'])
def save_file():
    res = {
        'status': 'ok',
        'url': '',
        'info': ''
    }
    file_name = str(uuid.uuid4())
    image_file = request.files.get('file')
    p = re.compile(r'.*?\.(gif|jpg|jpeg|png)$')
    match = p.match(image_file.filename, re.I)
    if not match:
        res.update(status='fail', info=u'图片格式不支持')
        return jsonify(res)
    file_id = new_fs.save_file(file_name, image_file.read(), content_type=image_file.content_type)
    res.update(status='ok', url=url_for('frontend.get_file', file_id=file_id))
    return jsonify(res)


@frontend_bp.route('/file/<file_id>')
def get_file(file_id):
    target_file = new_fs.get_file(file_id)
    res = make_response(target_file[0].read())
    res.headers['Content-Type'] = target_file[1].get('content_type', '')
    return res
