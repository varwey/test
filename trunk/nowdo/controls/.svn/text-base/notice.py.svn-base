# -*- coding: utf-8 -*-
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.base import Base, id_generate

from nowdo.utils.nowdo_logger import nowdo_logger as logger
from nowdo.utils.paginator import pagination_or_not

__author__ = 'lhfu'


class Notice(Base):
    __tablename__ = 'notice'

    PER_PAGE = 15

    type_list = range(2)
    NOTICE_TYPE_FOLLOW, NOTICE_TYPE_COMMENT = type_list

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    type = SA.Column(BIGINT(unsigned=True), nullable=False)
    sender_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey("account.id"), nullable=False)
    receiver_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey("account.id"), nullable=False)
    is_read = SA.Column(SA.Boolean, default=False, nullable=False)

    related_event_id = SA.Column(BIGINT(unsigned=True), nullable=True)

    @classmethod
    def create(cls, db_session, type, sender_id, receiver_id, related_event_id):
        new_notice = cls(type=type, sender_id=sender_id, receiver_id=receiver_id, related_event_id=related_event_id)

        db_session.add(new_notice)
        db_session.commit()

    def get_notice_str(self, notice):
        if notice.type == self.NOTICE_TYPE_FOLLOW:
            notice_str = self.sender.display_name + "关注了你"
        elif notice.type == self.NOTICE_TYPE_COMMENT:
            notice_str = self.sender.display_name + "评论了你的文章"

        return notice_str

    @classmethod
    def get_notice_list(cls, db_session, receiver_id, page=None, per_page=None):
        trends_query = db_session.query(Notice).filter(Notice.receiver_id == receiver_id).order_by(cls.created_date.desc())
        return pagination_or_not(trends_query, page, per_page, Notice.PER_PAGE)