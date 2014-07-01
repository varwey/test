# coding=utf-8
"""
created by SL on 14-3-25

标签
"""
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql.functions import count

from nowdo.controls.base import Base, id_generate
from nowdo.utils.paginator import pagination_or_not
from nowdo.utils.session import session_cm

__author__ = 'SL'


class Tag(Base):
    __tablename__ = 'tag'

    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    tag_name = SA.Column(SA.String(64), nullable=False, index=True)
    hot = SA.Column(SA.Integer, nullable=False, default=1)

    def to_dict(self):
        return {"id": self.id, "tag_name": self.tag_name}

    def tasks(self, limit=3):
        from nowdo.controls.crowd_source_task import CrowdSourceTask, CrowdSourceTaskTagRel
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            task_query = self.session.query(CrowdSourceTask).join(CrowdSourceTaskTagRel)\
                .filter(CrowdSourceTaskTagRel.tag_id == self.id)\
                .order_by(CrowdSourceTask.created_date.desc())\
                .limit(limit)
            return task_query.all()

    @staticmethod
    def task_tags(db_session, featured=False, min_task_count=1, page=None, per_page=None):
        """
        包含任务的标签列表
            :featured 是否只显示有精选主题的标签
            :min_task_count 最小的主题数
        """
        from nowdo.controls.crowd_source_task import CrowdSourceTaskTagRel
        tag_query = db_session.query(Tag, count(CrowdSourceTaskTagRel.id).label('task_count'))\
            .join(Tag.tag_rel_list)
        if featured:
            tag_query = tag_query.filter(CrowdSourceTaskTagRel.is_featured == True)
        tag_query = tag_query.group_by(Tag.id).having(count() >= min_task_count).order_by('task_count desc')
        return pagination_or_not(tag_query, page=page, per_page=per_page, default_per_page=Tag.PER_PAGE)

    @staticmethod
    def get_by_name(db_session, tag_name):
        return db_session.query(Tag).filter(Tag.tag_name == tag_name).first()

    @classmethod
    def search_by_name(cls, db_session, search_name, max=5):
        query = db_session.query(Tag).order_by(cls.created_date.desc())
        if search_name:
            query = query.filter(cls.tag_name.like("%" + search_name + "%"))

        if max:
            query = query.limit(max)

        return query.all()

    @staticmethod
    def add_tags(db_session, tag_list):
        if not tag_list:
            return []
        existed_tags = db_session.query(Tag).filter(Tag.tag_name.in_(tag_list)).all()
        existed_tag_names = [t.tag_name for t in existed_tags]
        new_tag_names = list(set(tag_list) - set(existed_tag_names))

        for tag in existed_tags:
            tag.hot += 1

        for new_tag_name in new_tag_names:
            tag = Tag(tag_name=new_tag_name)
            existed_tags.append(tag)
        return existed_tags

    @staticmethod
    def update_tags(db_session, tags_str, origin_tags=None):
        """
        更新标签列表，返回新的标签列表
            :origin_tags
                原来的标签对象列表
            :tags_str
                新的标签字符串，如：'文学，搞笑，垃圾'
        """
        tag_list = tags_str.replace(u'，', ',').split(',')
        if not origin_tags:
            return Tag.add_tags(db_session, tag_list)

        # 此次更新需要移除的标签
        removed_tags = filter(lambda x: x.tag_name not in tag_list, origin_tags)
        # 此次更新需要保留的标签
        reserved_tags = list(set(origin_tags) - set(removed_tags))

        # 将移除的标签热度降低
        for removed_tag in removed_tags:
            removed_tag.down_degree()

        # 此次更新需要新加入的标签
        new_tags = list(set(tag_list) - set([t.tag_name for t in origin_tags]))
        tags = Tag.add_tags(db_session, new_tags)

        reserved_tags.extend(tags)
        return reserved_tags

    @staticmethod
    def hot_tags(db_session, limit=20):
        tags = db_session.query(Tag).order_by('hot desc').limit(limit).all()
        return tags

    def down_degree(self):
        """
        降温
        """
        if self.hot > 0:
            self.hot -= 1
        if self.hot <= 0:
            self.session.delete(self)

    def up_degree(self):
        """
        升温
        """
        self.hot += 1