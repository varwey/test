# coding=utf-8
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, Boolean

from flask import url_for
from flask.ext.login import UserMixin
from flask.ext.babel import gettext as _
from werkzeug.security import generate_password_hash, check_password_hash
from nowdo.controls.account_property import AccountProperty
from nowdo.controls.base import Base, id_generate
# from cooperation.tasks.mail import send_mail
from nowdo.utils import memcache_tool
from nowdo.utils.avatar import get_avatar_url
from nowdo.utils.sendmail.mail_sender import send_mail
from nowdo.utils.sendmail.send_account_mail import get_activate_email_content, get_lost_psd_email_content, get_reg_invitation_content
from nowdo.utils.session import session_cm
from nowdo.utils.string_utils import get_random_key


class Account(Base, UserMixin):
    __tablename__ = 'account'
    PER_PAGE = 30

    ACCOUNT_TYPE_CROWD_SOURCE = 'crowd_source_account'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    name = SA.Column(VARCHAR(128, charset='latin1', collation='latin1_general_cs'), unique=True, nullable=False)
    email = SA.Column(String(128), unique=True, nullable=False)
    display_name = SA.Column(String(128))
    active = SA.Column(Boolean, default=True, nullable=False)
    is_admin = SA.Column(Boolean, default=False, nullable=False)
    pw_hash = SA.Column(String(128))

    # 账号类型
    type = SA.Column(String(128))

#     ###################################################################
#     #: Relationships.
#     account_setting = relationship('AccountSetting', backref='account', uselist=False, cascade='delete')
#     account_roles = relationship('AccountRole', backref='account')
    account_properties = relationship('AccountProperty', backref='account', cascade='delete')
#     ###################################################################

    group_role = None
#

    @property
    def nickname(self):
        return self.display_name or self.email

    def avatar_url(self, default_avatar_size=50):
        with session_cm() as account_session:
            if not self.session:
                account_session.add(self)
            avatar_id = self.get_property_value('avatar_id')
            if avatar_id:
                return url_for('frontend.get_file', file_id=avatar_id)
            else:
                return 'http://www.gravatar.com/avatar/000?d=mm&f=y&s=' \
                       + str(default_avatar_size)
            # return get_avatar_url(self.email, size=50)

    def sized_avatar_url(self, size):
        return get_avatar_url(self.email, size)

    def get_property_obj(self, key):
        return self.session.query(AccountProperty).filter(AccountProperty.account_id == self.id,
                                                          AccountProperty.key == key).first()

    def get_property_value(self, key):
        obj = self.get_property_obj(key)
        return obj.value if obj else ""

    def joined(self, group_id):
        from nowdo.controls.group import GroupUserRel
        with session_cm() as db_session:
            return db_session.query(GroupUserRel).filter(GroupUserRel.group_id == group_id,
                                                         GroupUserRel.user_id == self.id).first()

    def followed(self, user_id):
        from nowdo.controls.follows import Follow
        with session_cm() as db_session:
            return db_session.query(Follow).filter(Follow.target_id == user_id,
                                                   Follow.user_id == self.id).first()
    @property
    def followd_count(self):
        from nowdo.controls.follows import Follow
        with session_cm() as db_session:
            return db_session.query(Follow).filter(Follow.user_id == self.id).count()

    @property
    def has_mail(self):
        from nowdo.controls.mail import Mail
        with session_cm() as db_session:
            return db_session.query(Mail).filter(Mail.receiver_id == self.id,
                                                 Mail.is_read == False).count() > 0

    @property
    def notice_number(self):
        from nowdo.controls.notice import Notice
        with session_cm() as db_session:
            return db_session.query(Notice).filter(Notice.receiver_id == self.id,
                                                   Notice.is_read == False).count()

    def set_property_with_dict(self, data):
        for key, value in data.items():
            self.set_property(key, value)

    def set_property(self, key, value):
        property_tmp = AccountProperty(account=self, key=key, value=value)
        self.session.add(property_tmp)

    def update_property(self, key, value):
        property_tmp = self.get_property_obj(key)
        if property_tmp:
            property_tmp.value = value
        else:
            property_tmp = AccountProperty(account=self, key=key, value=value)
            self.session.add(property_tmp)

    def get_activation_email_resend_url(self):
        return url_for('account.resend_email', email=self.email, type="activate")

    def get_reset_pwd_email_resend_url(self):
        return url_for('account.resend_email', email=self.email, type="reset_pwd")
#

    def set_password(self, pw, **kwargs):
        if kwargs.get('key'):
            if memcache_tool.memcache_get(kwargs.get('key')) == self.email:
                memcache_tool.memcache_set(kwargs.get('key'), None)
        self.pw_hash = generate_password_hash(pw, salt_length=16)
#

    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)
#

    def is_active(self):
        return self.active == True

    def is_super_admin(self):
        return self.is_admin
#
#     def group_for_project(self, project):
#         """
#         用户在指定项目中所属的用户组
#         1. 获取用户在指定项目中的角色，即用户组的ID
#         2. 获取这些ID对应的用户组
#         """
#         roles = self.role_for_project(project)
#         account_session = get_router_session()
#         groups = account_session.query(Group).filter(Group.identity.in_(roles)).all()
#         account_session.close()
#         return groups
#
#     def member_of(self, project):
#         ac_ids = [ar.service_id for ar in self.account_roles]
#
#         return project.id in ac_ids
#
#     def is_crowd_source_platform_user(self):
#         return self.type == Account.ACCOUNT_TYPE_CROWD_SOURCE
#
#     def is_project_admin(self, project):
#         #return 'project_admin' in self.role_for_project(project) or self.is_project_creator(project)
#         return ROLE_SERVICE_ADMIN in self.role_for_project(project) or self.is_project_creator(project)
#
#     def is_project_creator(self, project):
#         #return 'project_creator' in self.role_for_project(project)
#         # 新的权限管理中取出了创建者，创建者即为管理员，此举只为兼容
#         return ROLE_SERVICE_ADMIN in self.role_for_project(project)
#
#     def is_project_member(self, project):
#         return ROLE_MEMBER in self.role_for_project(project)
#
#     def is_translator(self, project):
#         return ROLE_TRANSLATOR in self.role_for_project(project)
#

    def i_lost_pw(self, **kwargs):
        # 1. 生成key
        key = get_random_key()
        memcache_tool.memcache_set(key, self.email, time=3600)
        kwargs.update(key=key, id=self.id, name=self.name or u'用户')
        # 2. 组织邮件内容
        content = get_lost_psd_email_content(**kwargs)
        # 3. 发送邮件
        send_mail(MailType.SUBJECT_LOST_PW, content, self.email)

    def send_register_mail(self, **kwargs):
        # 1. 生成key
        key = get_random_key()
        memcache_tool.memcache_set(key, self.email, time=3600)
        kwargs.update(key=key, id=self.id, name=self.name or u'用户')
        # 2. 组织邮件内容
        content = get_activate_email_content(**kwargs)
        # 3. 发送邮件
        send_mail(MailType.SUBJECT_REGISTER, content, self.email)

    @classmethod
    def send_reg_invitation_mail(cls, **kwargs):
        # 1. 组织邮件内容
        content = get_reg_invitation_content(**kwargs)
        # 2. 发送邮件
        send_mail(MailType.SUBJECT_REG_INVITATION, content, kwargs['email'])

    def set_active(self, status):
        self.active = status
#
#     def to_dict(self):
#         return {
#             'id': str(self.id),
#             'name': self.name,
#             'email': self.email,
#             #'qq': self.qq,
#             'display_name': self.display_name,
#             'active': self.active,
#             'is_admin': self.is_admin,
#             'type': self.type,
#             'crowd_source_type_str': Account.ACCOUNT_TYPE_CROWD_SOURCE,
#             'creation': self.created_date.strftime('%Y-%m-%d %H:%M'),
#             'modification': self.modified_date.strftime('%Y-%m-%d %H:%M')
#         }
#
#
# class EmailNotExist(Exception):
#     pass
#
#
# class BadPasswordCode(Exception):
#     """
#     修改密码验证码错误
#     """
#     pass
#
#
# import random
# import string
#
#
# def _get_random_key():
#     return ''.join([random.choice(string.letters) for i in xrange(48)])
#
#
# def email_exists(session, email):
#     return session.query(Account).filter(Account.email == email).count() >= 0
#
#
# #########################################################################
# # 密码找回
# def i_lost_pw(session, email):
#     if not email_exists(session, email):
#         raise EmailNotExist()
#     key = _get_random_key()
#     memcache_tool.memcache_set(key, email)
#     return key
#
#
# def check_pw_code(pw_code):
#     return memcache_tool.memcache_get(pw_code)
#
#
# def change_password(session, pw_code, new_password):
#     code = check_pw_code(pw_code)
#     if not code:
#         raise BadPasswordCode()
#     account = session.query(Account).filter(Account.email == code).one()
#     account.set_password(new_password)
#
#
# def check_mail(session, email, func, type):
#     key = i_lost_pw(session, email)
#     msg2send = func(key, email=email)
#     send_mail.delay(MailType.SUBJECT_REGISTER, msg2send, to=[email, ])
#
#
# def activate(session, pw_code):
#     code = check_pw_code(pw_code)
#     if not code:
#         raise BadPasswordCode()
#     account = session.query(Account).filter(Account.email == code).one()
#     account.set_active(True)
#     memcache_tool.memcache_set(pw_code, None)
#
#
class MailType:
    #邮件相关类型类型
    SUBJECT_LOST_PW = _(u'脑洞-找回密码')
    SUBJECT_REGISTER = _(u'脑洞-帐号激活')
    SUBJECT_FREE_TRIAL_ZH = _(u'脑洞-试用')
    SUBJECT_FREE_TRIAL_EN = _(u'NowDo-Trial')
    SUBJECT_TRIAL_EXPIRE = _(u'脑洞-试用到期提醒')
    SUBJECT_BUSINESS_INFO = _(u'脑洞-客户经理/NowDo-Your Supervisor')
    SUBJECT_FREE_TRIAL_NOTICE = _(u'脑洞-客户试用通知')
    SUBJECT_REG_INVITATION = _(u'脑洞-邀请注册')