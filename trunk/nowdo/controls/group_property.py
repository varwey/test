# -*- coding=utf-8 -*-
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.base import Base, id_generate
import sqlalchemy as SA
from nowdo.utils.session import session_cm

__author__ = 'SL'


class GroupProperty(Base):
    """
    小组属性表
    例如小组头像ID等信息
    """

    SERVICE_ID, = ('service_id', )

    ##########################################################################
    # table
    __tablename__ = 'group_property'

    #: Columns
    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    group_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey("group.id"), nullable=False)
    key = SA.Column(SA.String(128), nullable=False)
    value = SA.Column(SA.String(512))

    ##########################################################################

    @classmethod
    def groups_has_property(cls, key, value):
        with session_cm() as account_session:
            property_list = account_session.query(cls)\
                .filter(cls.key == key, cls.value == value)\
                .options(joinedload('group'))\
                .all()
            users = [p.account for p in property_list]
            return users