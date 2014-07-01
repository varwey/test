# coding=utf-8
"""
created by SL on 14-3-6

小组
"""
from flask.ext.login import current_user
from flask import url_for
import sqlalchemy as SA
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import Table
from sqlalchemy.sql.expression import or_
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.sql.functions import count
from sqlalchemy.types import String, Integer

from nowdo.controls.base import Base, id_generate
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.group_property import GroupProperty
from nowdo.controls.tag import Tag
from nowdo.controls.trends import Trends
from nowdo.controls.account import Account
from nowdo.utils.paginator import SQLAlchemyPaginator, pagination_or_not
from nowdo.utils.session import session_cm
from nowdo.utils.trends_utils import TREND_ACTION_CREATE, TREND_TARGET_TYPE_GROUP


__author__ = 'SL'

# 小组与标签的关系表
GroupTagRelTable = Table('group_tag_rel', Base.metadata,
                         SA.Column('group_id', BIGINT(unsigned=True), SA.ForeignKey('group.id')),
                         SA.Column('tag_id', BIGINT(unsigned=True), SA.ForeignKey('tag.id')))

# 小组与主题的关系表
GroupTaskRelTable = Table('group_task_rel', Base.metadata,
                          SA.Column('group_id', BIGINT(unsigned=True), SA.ForeignKey('group.id')),
                          SA.Column('task_id', BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id')))


class Group(Base):
    __tablename__ = 'group'

    PER_PAGE = 30

    # 模式：自由模式（个人），战队模式
    MODE_PERSONAL, MODE_TEAM = range(2)

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    group_name = SA.Column(SA.String(64), nullable=False)
    group_address = SA.Column(SA.String(64))
    group_description = SA.Column(SA.TEXT, nullable=False)
    # group_tags = SA.Column(SA.String(1024), nullable=False)
    creator_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    mode = SA.Column(SA.Integer, default=MODE_PERSONAL)

    members = relationship("GroupUserRel", backref='group')
    # tasks = relationship("CrowdSourceTask", backref='group', order_by="desc(CrowdSourceTask.created_date)")
    topics = relationship("Topic", backref='group', order_by="desc(Topic.created_date)")
    group_properties = relationship('GroupProperty', backref='group', cascade='delete')

    tags = relationship('Tag', secondary=GroupTagRelTable, backref='groups')
    tasks = relationship('CrowdSourceTask',
                         secondary=GroupTaskRelTable,
                         lazy="dynamic",
                         backref=backref('group', uselist=False),
                         order_by="desc(CrowdSourceTask.created_date)")

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'group_description': self.group_description
        }

    def get_tasks(self, limit=3):
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            return self.tasks.limit(limit)

    def avatar_url(self, default_avatar_size=50):
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            avatar_id_prop = self.get_property('avatar_id')
            if avatar_id_prop:
                return url_for('frontend.get_file', file_id=avatar_id_prop.value)
            else:
                return 'http://www.gravatar.com/avatar/000?d=mm&f=y&s=' \
                       + str(default_avatar_size)

    @property
    def creator(self):
        from nowdo.controls.account import Account
        with session_cm() as account_session:
            return account_session.query(Account).get(self.creator_id)

    # @property
    # def tags(self):
    #     tmp_tags_str = self.group_tags.replace(u'，', ',')
    #     return tmp_tags_str.split(',')

    def member_list(self):
        members = self.members
        member_id_rel_map = dict([(member.user_id, member) for member in members])
        with session_cm() as account_session:
            member_list = account_session.query(Account).filter(Account.id.in_(member_id_rel_map.keys())).all()
            for m in member_list:
                m.group_role = member_id_rel_map[m.id].role
            return member_list

    def get_member(self, user_id):
        with session_cm() as account_session:
            user = account_session.query(Account).get(user_id)
            group_role = self.session.query(GroupUserRel.role).filter(GroupUserRel.user_id == user_id,
                                                                      GroupUserRel.group_id == self.id).scalar()
            if not user or not group_role:
                return None
            else:
                user.group_role = group_role
                return user

    def get_property(self, key):
        return self.session.query(GroupProperty).filter(GroupProperty.key == key,
                                                        GroupProperty.group_id == self.id).first()

    def set_property(self, key, value):
        prop = self.get_property(key)
        if prop:
            prop.value = value
        else:
            group_property = GroupProperty(key=key, value=value, group=self)
            self.session.add(group_property)
        self.session.commit()

    def is_creator(self, user):
        """
        判断用户是否为创建者
        """
        return self.creator_id == user.id

    def is_admin(self, user):
        """
        判断用户是否为小组的管理者
        """
        if not user.is_authenticated():
            return False
        if self.session.query(GroupUserRel)\
            .filter(GroupUserRel.group_id == self.id,
                    GroupUserRel.user_id == user.id,
                    or_(GroupUserRel.role == GroupUserRel.GROUP_ROLE_CREATOR,
                        GroupUserRel.role == GroupUserRel.GROUP_ROLE_MANAGER)).first():
            return True
        return False

    def is_member(self, user, include_creator=True):
        """
        判断用户是否为小组成员
        """
        if not user.is_authenticated():
            return False
        rel = self.session.query(GroupUserRel).filter(GroupUserRel.group_id == self.id,
                                                      GroupUserRel.user_id == user.id).first()
        if rel:
            if not include_creator and rel.user_id == self.creator_id:
                return False
            return True
        return False

    def add_member(self, user):
        """
        添加成员
        """
        user_rel = GroupUserRel(group_id=self.id, user_id=user.id, user_email=user.email)
        self.session.add(user_rel)
        self.session.commit()

    def remove_member(self, user):
        """
        移除成员
        """
        user_rel = self.session.query(GroupUserRel)\
            .filter(GroupUserRel.group_id == self.id, GroupUserRel.user_id == user.id).first()
        if user_rel:
            self.session.delete(user_rel)
            self.session.commit()

    def toggle_join(self, user):
        """
        有则退出，无则加入
        """
        user_rel = self.session.query(GroupUserRel) \
            .filter(GroupUserRel.group_id == self.id, GroupUserRel.user_id == user.id).first()
        if user_rel:
            self.session.delete(user_rel)
            self.session.commit()
            return 'quit'
        else:
            user_rel = GroupUserRel(group_id=self.id, user_id=user.id, user_email=user.email)
            self.session.add(user_rel)
            self.session.commit()
            return 'joined'

    def add_manager(self, user_id):
        """
        将某个成员晋升为管理员
        """
        return self.change_role(user_id, GroupUserRel.GROUP_ROLE_MANAGER)

    def remove_manager(self, user_id):
        """
        取消某个管理员的管理员资格
        """
        return self.change_role(user_id, GroupUserRel.GROUP_ROLE_MEMBER)

    def change_role(self, user_id, role):
        """
        更换用户角色
        """
        try:
            user_rel = self.session.query(GroupUserRel).filter(GroupUserRel.group_id == self.id,
                                                               GroupUserRel.user_id == user_id).one()
            if user_rel:
                user_rel.role = role
                self.session.commit()
                return True
        except NoResultFound:
            return False

    def available_tasks(self):
        if current_user.is_authenticated() and current_user.id == self.creator_id:
            tasks = self.tasks
        else:
            tasks = self.session.query(CrowdSourceTask) \
                .join(CrowdSourceTask.group)\
                .filter(CrowdSourceTask.status == CrowdSourceTask.STATUS_TRANSLATING,
                        Group.id == self.id)\
                .order_by(CrowdSourceTask.created_date.desc()).all()
        return tasks

    def update_common_info(self, group_name, group_description, group_tags_str):
        self.tags = Tag.update_tags(self.session, group_tags_str, self.tags)
        self.group_name = group_name
        self.group_description = group_description
        self.session.commit()

    @classmethod
    def create_group(cls, group_name, group_description, group_tags, creator_id=None):
        if not creator_id and current_user.is_authenticated():
            creator_id = current_user.id

        with session_cm() as db_session:
            group = cls(group_name=group_name,
                        group_description=group_description,
                        creator_id=creator_id)

            tags = Tag.update_tags(db_session, group_tags)
            group.tags = tags
            user_rel = GroupUserRel(user_id=current_user.id,
                                    user_email=current_user.email,
                                    role=GroupUserRel.GROUP_ROLE_CREATOR)
            group_member_list = group.members
            group.members = group_member_list.append(user_rel) if group_member_list else [user_rel, ]
            db_session.add(group)
            db_session.commit()
            Trends.add_trends(current_user, TREND_ACTION_CREATE, TREND_TARGET_TYPE_GROUP, group)

    @staticmethod
    def tagged_group_ids(db_session, tag, return_list=False):
        """
        带有标签 tag 的小组
        return_list:
            为 True 表示返回小组ID的列表
            为 False 只返回 Query 对象
        """
        tagged_group_id_query = db_session.query(Group.id.distinct())
        if tag:
            tagged_group_id_query = tagged_group_id_query.join(Group.tags) \
                .filter(Tag.tag_name == tag)
        if return_list:
            return [tg.id for tg in tagged_group_id_query.all()]
        return tagged_group_id_query

    @staticmethod
    def _hot_groups(db_session, tag=None, page=None, per_page=None, with_current_user_joined=True):
        group_query = db_session.query(Group, count(GroupUserRel.group_id).label('joined_count'))
        if not with_current_user_joined and current_user.is_authenticated():
            joined_group_id_query = db_session.query(GroupUserRel.group_id) \
                .filter(GroupUserRel.user_id == current_user.id).subquery()
            group_query = group_query.filter(Group.id.notin_(joined_group_id_query))
        if tag:
            group_query = group_query.join(Group.tags) \
                .filter(Tag.tag_name == tag)
        group_query = group_query.outerjoin(GroupUserRel) \
            .group_by(GroupUserRel.group_id) \
            .order_by('joined_count desc').options(joinedload('tags'))

        return pagination_or_not(group_query, page, per_page, Group.PER_PAGE)

    @staticmethod
    def joined_groups(db_session, user, page=None, per_page=None):
        per_page = Group.PER_PAGE if per_page is None else per_page
        group_query = db_session.query(Group) \
            .outerjoin(GroupUserRel) \
            .filter(GroupUserRel.user_id == user.id).order_by(Group.created_date.desc())

        if page:
            paginator = SQLAlchemyPaginator(group_query, per_page=per_page)
            return paginator.page(page)
        else:
            return group_query.all()

    @staticmethod
    def explore_hot_groups(db_session, tag=None, page=None, per_page=None):
        return Group._hot_groups(db_session, tag, page, per_page, False)

    @staticmethod
    def hot_groups(db_session, tag=None, page=None, per_page=None):
        return Group._hot_groups(db_session, tag, page, per_page)

    @staticmethod
    def latest_groups(db_session, page=None, per_page=None, with_current_user_joined=True):
        group_query = db_session.query(Group, count(GroupUserRel.group_id).label('joined_count')) \
            .outerjoin(GroupUserRel)
        if not with_current_user_joined and current_user.is_authenticated():
            joined_group_id_query = db_session.query(GroupUserRel.group_id) \
                .filter(GroupUserRel.user_id == current_user.id).subquery()
            group_query = group_query.filter(Group.id.notin_(joined_group_id_query))
        group_query = group_query.group_by(GroupUserRel.group_id)\
            .order_by('group.created_date desc')
        return pagination_or_not(group_query, page, per_page, Group.PER_PAGE)


class GroupUserRel(Base):
    """
    小组成员关系表
    """
    __tablename__ = 'group_user_rel'

    GROUP_ROLE_CREATOR, GROUP_ROLE_MANAGER, GROUP_ROLE_MEMBER = range(3)

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    group_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey("group.id"))
    user_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    user_email = SA.Column(String(128), nullable=False)
    role = SA.Column(Integer, nullable=False, default=GROUP_ROLE_MEMBER)

    @property
    def role_name(self):
        role_map = {
            GroupUserRel.GROUP_ROLE_CREATOR: u'创建者',
            GroupUserRel.GROUP_ROLE_MANAGER: u'管理员',
            GroupUserRel.GROUP_ROLE_MEMBER: u'成员'
        }
        return role_map[self.role]