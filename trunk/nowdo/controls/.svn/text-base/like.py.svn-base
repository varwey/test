# coding=utf-8
"""
created by SL on 14-4-18

喜欢主题
"""
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship

from nowdo.controls.base import Base, id_generate
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.trends import Trends
from nowdo.utils.trends_utils import TREND_ACTION_LIKE, TREND_TARGET_TYPE_TASK

__author__ = 'SL'


class LikeRel(Base):
    """
    用户喜欢某个主题的关系表
    """
    __tablename__ = 'like_rel'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    user_id = SA.Column(BIGINT(unsigned=True), default=True, index=True)
    task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id'))

    task = relationship('CrowdSourceTask', backref='like_rel_list')

    @staticmethod
    def like(db_session, user, task):
        """
        user 喜欢 task
        """
        like_rel = LikeRel(user_id=user.id, task_id=task.id)
        db_session.add(like_rel)
        db_session.commit()
        Trends.add_trends(user, TREND_ACTION_LIKE, TREND_TARGET_TYPE_TASK, task)

    @staticmethod
    def has_like(db_session, user, task):
        """
            判断 user 是否喜欢 task
        """
        return db_session.query(LikeRel)\
            .filter(LikeRel.user_id == user.id,
                    LikeRel.task_id == task.id).first()

    @staticmethod
    def toggle_like(db_session, user, task):
        """
        喜欢或者取消喜欢
        """
        like_rel = LikeRel.has_like(db_session, user, task)
        if like_rel:
            db_session.delete(like_rel)
            Trends.remove_trends(db_session, target_id=task.id, user_id=like_rel.user_id, action=TREND_ACTION_LIKE)
            res = 'unlike'
        else:
            LikeRel.like(db_session, user, task)
            res = 'like'
        db_session.commit()

        return res

    @staticmethod
    def liked_tasks(db_session, user):
        """
        user 喜欢的主题
        """
        return db_session.query(CrowdSourceTask).join(CrowdSourceTask.like_rel_list)\
            .filter(LikeRel.user_id == user.id).all()