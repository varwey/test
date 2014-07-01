# coding=utf-8
"""
created by SL on 14-3-27

关注关系
"""
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT

from nowdo.controls.base import Base, id_generate
from nowdo.controls.account import Account
from nowdo.controls.notice import Notice
from nowdo.utils.paginator import pagination_or_not
from nowdo.utils.session import session_cm

__author__ = 'SL'


class Follow(Base):
    """
    用户关注信息表
    """

    __tablename__ = 'follow'

    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    user_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    target_id = SA.Column(BIGINT(unsigned=True), nullable=False)

    @staticmethod
    def follow(user, target_user):
        with session_cm() as db_session:
            follow = Follow(user_id=user.id, target_id=target_user.id)
            db_session.add(follow)
            db_session.commit()

    @staticmethod
    def toggle_follow(user, target_user):
        with session_cm() as db_session:
            is_followed = db_session.query(Follow).filter(Follow.user_id == user.id,
                                                          Follow.target_id == target_user.id).first()
            if is_followed:
                db_session.delete(is_followed)
                db_session.commit()
                return 'un_followed'
            else:
                follow = Follow(user_id=user.id, target_id=target_user.id)
                db_session.add(follow)
                db_session.commit()
                Notice.create(db_session, type, user.id, target_user.id, None)
                return 'followed'

    @staticmethod
    def followed_user_ids(db_session, user):
        """
        user 关注的用户的ID
        """
        return [f[0] for f in db_session.query(Follow.target_id).filter(Follow.user_id == user.id)]

    @staticmethod
    def followed_users(db_session, user, page=None, per_page=None):
        """
        user 关注的用户列表
        """
        followed_list = db_session.query(Follow).filter(Follow.user_id == user.id).all()
        followed_user_ids = [f.target_id for f in followed_list]
        with session_cm() as account_session:
            user_query = account_session.query(Account).filter(Account.id.in_(followed_user_ids))
            return pagination_or_not(user_query, page, per_page, default_per_page=Follow.PER_PAGE)

    @staticmethod
    def followers(db_session, user, page=None, per_page=None):
        """
        关注 user 的用户列表
        """
        follow_list = db_session.query(Follow).filter(Follow.target_id == user.id).all()
        follower_ids = [f.user_id for f in follow_list]
        with session_cm() as account_session:
            user_query = account_session.query(Account).filter(Account.id.in_(follower_ids))
            return pagination_or_not(user_query, page, per_page)