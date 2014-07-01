# -*- coding=utf-8 -*-
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.base import Base, id_generate
import sqlalchemy as SA
from nowdo.utils.session import session_cm

__author__ = 'SL'


class AccountProperty(Base):
    """
    帐户属性表
    """

    QZGS_TEAM, FORUM_ID, LOCALE = ('team', 'forum_id', 'locale')

    ##########################################################################
    # table
    __tablename__ = 'account_property'

    #: Columns
    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    account_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey("account.id"), nullable=False)
    key = SA.Column(SA.String(128), nullable=False)
    value = SA.Column(SA.String(512))

    ##########################################################################

    @classmethod
    def users_has_property(cls, key, value):
        with session_cm() as account_session:
            property_list = account_session.query(AccountProperty)\
                .filter(AccountProperty.key == key, AccountProperty.value == value)\
                .options(joinedload('account'))\
                .all()
            users = [p.account for p in property_list]
            return users