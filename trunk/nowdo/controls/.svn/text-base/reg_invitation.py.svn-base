# -*- coding: utf-8 -*-
import traceback
import datetime
import sqlalchemy as SA
from sqlalchemy.dialects.mysql.base import BIGINT
from sqlalchemy.types import String
from nowdo.controls.base import Base, id_generate
from nowdo.utils.paginator import pagination_or_not

__author__ = 'lhfu'


class RegInvitation(Base):
    """
    注册邀请
    """
    __tablename__ = 'reg_invitation'
    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    inviter_id = SA.Column(BIGINT(unsigned=True), index=True, nullable=False)
    invitee_email = SA.Column(String(128), index=True, nullable=False)

    invite_date = SA.Column(SA.DateTime, nullable=True, default=datetime.datetime.now)

    @classmethod
    def create(cls, db_session, inviter_id, invitee_email):
        reg_invitation = cls(
            inviter_id=inviter_id,
            invitee_email=invitee_email,
        )
        db_session.add(reg_invitation)
        db_session.commit()
        return reg_invitation

    @classmethod
    def get_invitees(cls, db_session, inviter_id, page=None, per_page=None):
        invitee_query = db_session.query(cls).filter(cls.inviter_id == inviter_id).order_by(cls.invite_date.desc())

        return pagination_or_not(invitee_query, page=page, per_page=per_page, default_per_page=cls.PER_PAGE)