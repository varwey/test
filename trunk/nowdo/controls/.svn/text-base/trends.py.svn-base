# coding=utf-8
"""
created by SL on 14-3-11
"""
from flask import url_for
from flask.ext.login import current_user
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.functions import count, max as sa_max
from nowdo.controls.base import Base, id_generate
from nowdo.controls.follows import Follow
from nowdo.controls.account import Account
from nowdo.utils.paginator import pagination_or_not
from nowdo.utils.session import session_cm
from nowdo.utils.trends_utils import TREND_TARGET_TYPE_GROUP, TREND_TARGET_TYPE_TOPIC, ACTION_MAP, TARGET_TYPE_MAP, TREND_TARGET_TYPE_TASK, TREND_TARGET_TYPE_COMMENT

__author__ = 'SL'


class Trends(Base):
    """
    动态表，记录：谁(user_id)干了(action)什么(target)
    记录NowDo中的动态
    1. 创建小组
    2. 创建话题
    3. 回复话题
    4. 发布任务
    5. 参与任务
    """
    __tablename__ = 'trends'
    PER_PAGE = 15

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    user_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    action = SA.Column(SA.String(64), nullable=False)
    target_type = SA.Column(SA.String(64), nullable=False)
    target_id = SA.Column(BIGINT(unsigned=True), nullable=False)

    @property
    def target_url(self):
        # 小组
        if self.target_type == TREND_TARGET_TYPE_GROUP:
            return url_for('group.group_home', group_id=self.target_id)
        # 话题
        if self.target_type == TREND_TARGET_TYPE_TOPIC:
            return url_for('group.topic_view', topic_id=self.target_id)
        # 主题
        if self.target_type == TREND_TARGET_TYPE_TASK:
            # return url_for('task.task_view', task_id=self.target_id)
            return url_for('task.task_translate', task_id=self.target_id) + '#read'
        # 评论
        if self.target_type == TREND_TARGET_TYPE_COMMENT:
            return url_for('group.comment_view', comment_id=self.target_id)

    @property
    def action_str(self):
        action_str = '%s了该%s' % \
                     (ACTION_MAP[self.action],
                      TARGET_TYPE_MAP[self.target_type])
        return action_str

    @staticmethod
    def add_trends(user, action, target_type, target):
        with session_cm() as db_session:
            trends = Trends(user_id=user.id, action=action, target_type=target_type, target_id=target.id)
            db_session.add(trends)
            db_session.commit()

    @staticmethod
    def remove_trends(db_session, target_id, user_id=None, action=None):
        """
        移除动态
        """
        trends_query = db_session.query(Trends).filter(Trends.target_id == target_id)
        if user_id:
            trends_query = trends_query.filter(Trends.user_id == user_id)
        if action:
            trends_query = trends_query.filter(Trends.action == action)
        trends_query.delete()

    @staticmethod
    def get_trends_list(db_session, user_ids=None, page=None, per_page=None):
        """
        获取动态列表
        同一个 target 只会显示一条最新的动态

        user_ids = None:
            所有的趋势
        user_ids != None:
            指定用户的趋势
        """
        sub_query = db_session.query(sa_max(Trends.created_date).label('max_date'),
                                     Trends.target_id.label('grouped_target_id'))\
            .group_by(Trends.target_id).subquery()

        trends_query = db_session.query(Trends)\
            .join(sub_query,
                  and_(Trends.created_date == sub_query.c.max_date,
                  Trends.target_id == sub_query.c.grouped_target_id))\
            .order_by(Trends.created_date.desc())
        if user_ids:
            trends_query = trends_query.filter(Trends.user_id.in_(user_ids))
        return pagination_or_not(trends_query, page, per_page, Trends.PER_PAGE)

    @staticmethod
    def get_trends_list_from_target_ids(target_ids, page=None, per_page=None):
        """
        通过动态目标ID，获取动态列表
        """
        if not target_ids:
            return None
        with session_cm() as db_session:
            trends_query = db_session.query(Trends)\
                .filter(Trends.target_id.in_(target_ids))\
                .order_by(Trends.created_date.desc())
            return pagination_or_not(trends_query, page, per_page, Trends.PER_PAGE)

    @staticmethod
    def passionate_users(page=None, per_page=8):
        """
        获取活跃的用户列表
            定义：与某个用户相关的动态越多，该用户的活跃度越高
        """
        with session_cm() as db_session:
            res = db_session.query(Trends.user_id, count(Trends.id).label('trends_count'))\
                .group_by(Trends.user_id)\
                .order_by('trends_count desc').all()
            user_id_trends_count_map = dict(res)
            user_query = db_session.query(Account)

            user_ids = user_id_trends_count_map.keys()
            if current_user.is_authenticated():
                # 过滤掉已经关注的用户
                followed_user_ids = [u.id for u in Follow.followed_users(db_session, current_user)]
                user_ids = list(set(user_ids) - set(followed_user_ids))
                # 过滤掉当前用户
                user_query = user_query.filter(Account.id != current_user.id)

            user_query = user_query.filter(Account.id.in_(user_ids))

            pagination_or_list = pagination_or_not(user_query, page, per_page)
            if isinstance(pagination_or_list, list):
                pagination_or_list = sorted(pagination_or_list,
                                            key=lambda x: user_id_trends_count_map[x.id],
                                            reverse=True)
            else:
                pagination_or_list.object_list = sorted(pagination_or_list.object_list,
                                                        key=lambda x: user_id_trends_count_map[x.id],
                                                        reverse=True)
            return pagination_or_list, user_id_trends_count_map

    def target_title(self, target):
        # 小组
        if self.target_type == TREND_TARGET_TYPE_GROUP:
            return target.group_name
        # 话题
        if self.target_type == TREND_TARGET_TYPE_TOPIC:
            return target.title
        # 任务
        if self.target_type == TREND_TARGET_TYPE_TASK:
            return target.name
        # 评论
        if self.target_type == TREND_TARGET_TYPE_COMMENT:
            return target.topic.title

    def target_content(self, target):
        # 小组
        if self.target_type == TREND_TARGET_TYPE_GROUP:
            return target.group_description
        # 话题
        if self.target_type == TREND_TARGET_TYPE_TOPIC:
            return target.content
        # 任务
        if self.target_type == TREND_TARGET_TYPE_TASK:
            return target.task_content
        # 评论
        if self.target_type == TREND_TARGET_TYPE_COMMENT:
            return target.content