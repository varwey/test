# coding=utf-8
"""
created by SL on 14-3-10
"""
from flask.ext.login import current_user

import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import count
from nowdo.controls.trends import Trends
from nowdo.controls.account import Account

from nowdo.controls.base import Base, id_generate
from nowdo.utils.escape_utils import deal_topic_content
from nowdo.utils.paginator import pagination_or_not
from nowdo.utils.session import session_cm
from nowdo.utils.trends_utils import TREND_ACTION_PUBLISH, TREND_TARGET_TYPE_TOPIC, TREND_TARGET_TYPE_COMMENT, TREND_ACTION_REPLY

__author__ = 'SL'


class Topic(Base):
    __tablename__ = 'topic'
    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    creator_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    group_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('group.id'))
    title = SA.Column(SA.String(255), nullable=False)
    content = SA.Column(SA.TEXT)

    comments = relationship('TopicComment', backref='topic')

    @property
    def creator(self):
        with session_cm() as account_session:
            return account_session.query(Account).get(self.creator_id)

    @staticmethod
    def create_topic(db_session, group, title, content):
        content = deal_topic_content(content)
        topic = Topic(group=group, title=title, content=content, creator_id=current_user.id)
        db_session.add(topic)
        db_session.commit()
        Trends.add_trends(current_user, TREND_ACTION_PUBLISH, TREND_TARGET_TYPE_TOPIC, topic)
        return topic

    @staticmethod
    def hot_topics(db_session, tag=None, page=None, per_page=None):
        from nowdo.controls.group import Group
        tagged_group_id_query = Group.tagged_group_ids(db_session, tag)

        topic_query = db_session.query(Topic, count(TopicComment.id).label('comment_count'))\
            .filter(Topic.group_id.in_(tagged_group_id_query.subquery()))\
            .outerjoin(Topic.comments)\
            .group_by(Topic.id)\
            .order_by('comment_count desc')
        return pagination_or_not(topic_query, page, per_page)

    @staticmethod
    def published_topics(db_session, user, page=None, per_page=None):
        """
        我发表的话题
        """
        topic_query = db_session.query(Topic).filter(Topic.creator_id == user.id).order_by(Topic.created_date.desc())
        return pagination_or_not(topic_query, page, per_page=per_page, default_per_page=Topic.PER_PAGE)

    @staticmethod
    def commented_topics(db_session, user, page=None, per_page=None):
        """
        我评论的话题
        """
        comment_sub_query = db_session.query(TopicComment.topic_id.distinct())\
            .filter(TopicComment.creator_id == user.id).subquery()
        topic_query = db_session.query(Topic).filter(Topic.id.in_(comment_sub_query)).order_by(Topic.created_date.desc())
        return pagination_or_not(topic_query, page, per_page, default_per_page=Topic.PER_PAGE)


class TopicComment(Base):
    __tablename__ = 'topic_comment'
    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    creator_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    topic_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('topic.id'), nullable=False)
    content = SA.Column(SA.TEXT)

    @property
    def creator(self):
        with session_cm() as account_session:
            return account_session.query(Account).get(self.creator_id)

    @staticmethod
    def create_comment(db_session, topic, content):
        comment = TopicComment(topic=topic, content=content, creator_id=current_user.id)
        db_session.add(comment)
        db_session.commit()
        Trends.add_trends(current_user, TREND_ACTION_REPLY, TREND_TARGET_TYPE_COMMENT, comment)
        return comment