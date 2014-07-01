# coding=utf-8
"""
created by SL on 14-3-6
"""
import datetime
import os

from flask.ext.login import current_user
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship, object_session, joinedload, backref
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import Table
from sqlalchemy.sql.expression import or_, and_, not_
from sqlalchemy.sql.functions import count, sum as sa_sum
from sqlalchemy.types import String
from flask import url_for
from nowdo.config import setting
from nowdo.config.celeryconfig import celery
from nowdo.controls.file import File
from nowdo.controls.glossary import Glossary
from nowdo.controls.image import Image
from nowdo.controls.notice import Notice
from nowdo.controls.tag import Tag
from nowdo.controls.trends import Trends
from nowdo.controls.account import Account
from nowdo.utils.date_utils import date_delta
from nowdo.utils.escape_utils import strip_tags, filter_images, deal_task_content

from nowdo.utils.kfile_api import kf_v1 as kf
from nowdo.controls.base import Base, id_generate
from nowdo.utils.paginator import pagination_or_not
from nowdo.utils.session import session_cm
from nowdo.utils.string_utils import get_random_filename
from nowdo.utils.trends_utils import TREND_ACTION_CREATE, TREND_TARGET_TYPE_TASK


__author__ = 'SL'

TaskTagRelTable = Table('task_tag_rel', Base.metadata,
                        SA.Column('task_id', BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id')),
                        SA.Column('tag_id', BIGINT(unsigned=True), SA.ForeignKey('tag.id')))

TaskGlossaryRelTable = SA.Table('task_glossary_rel', Base.metadata,
                                SA.Column('glossary_id',
                                          BIGINT(unsigned=True), SA.ForeignKey('glossary.id')),
                                SA.Column('task_id',
                                          BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id')))


class CrowdSourceTaskTagRel(Base):
    __tablename__ = 'crowd_source_task_tag_rel'
    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id', ondelete='cascade'))
    tag_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('tag.id'))
    # 是否精选
    is_featured = SA.Column(SA.Boolean, default=False)

    tag = relationship('Tag', backref='tag_rel_list', lazy='joined')

    @staticmethod
    def get_rel(db_session, task_id, tag_id):
        try:
            rel = db_session.query(CrowdSourceTaskTagRel)\
                .filter(CrowdSourceTaskTagRel.task_id == task_id,
                        CrowdSourceTaskTagRel.tag_id == tag_id).one()
            return rel
        except NoResultFound:
            return None

    @staticmethod
    def get_rel_list_by_tag_name(db_session, tag_name=None, featured=False, page=None, per_page=None):
        rel_query = db_session.query(CrowdSourceTaskTagRel).options(joinedload('task'))
        if tag_name:
            rel_query = rel_query.join(CrowdSourceTaskTagRel.tag).filter(Tag.tag_name == tag_name)
        if featured:
            rel_query = rel_query.filter(CrowdSourceTaskTagRel.is_featured == True)
        return pagination_or_not(rel_query, page=page, per_page=per_page, default_per_page=CrowdSourceTaskTagRel.PER_PAGE)

    @staticmethod
    def get_rel_with_task_count(db_session, page=None, per_page=None):
        tag_query = db_session.query(CrowdSourceTaskTagRel,
                                     count().label('task_count'))\
            .group_by(CrowdSourceTaskTagRel.tag_id).order_by('task_count desc')
        for rel, c in tag_query.all():
            print '--------------'
            print 'tag_id: %s, task_id: %s, task_count: %s' % (str(rel.tag_id), str(rel.task_id), str(c))
        return pagination_or_not(tag_query, page, per_page, default_per_page=30)


class CrowdSourceTaskContent(Base):

    __tablename__ = 'crowd_source_task_content'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id'))
    # 任务内容
    content = SA.Column(SA.Text)


class CrowdSourceTask(Base):
    __tablename__ = 'crowd_source_task'
    PER_PAGE = 30

    TASK_TYPE_TEXT, TASK_TYPE_IMAG = range(2)

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)

    # 初始化：可以阅读、可以开启翻译、可以编辑
    # 关闭：可以阅读、可以开启翻译、不能编辑
    # 翻译中：可以阅读、可以关闭翻译、不能编辑
    # 已完成：可以阅读、可以开启翻译、不能编辑
    STATUS_INIT, STATUS_CLOSED, STATUS_TRANSLATING, STATUS_FINISHED = range(4)

    name = SA.Column(SA.String(255), nullable=False)

    src_lang = SA.Column(SA.String(2), nullable=False)
    #: 目标语言
    tar_lang = SA.Column(SA.String(512), nullable=False)
    #: 已经完成的目标语言
    completed_tar_lang = SA.Column(SA.String(512))
    #: 状态: 初始，翻译中，翻译完成
    status = SA.Column(SA.SmallInteger, nullable=False, index=True, default=STATUS_INIT)
    # 任务包含的词条数
    entry_count = SA.Column(SA.Integer, default=0)
    # 任务包含的字数
    word_count = SA.Column(SA.Integer, default=0)
    # 任务创建人
    creator_id = SA.Column(BIGINT(unsigned=True), index=True, nullable=True)
    # 保留词
    reserved_words = SA.Column(SA.Text)
    # 任务描述
    description = SA.Column(SA.Text)
    # 开始日期
    start_date = SA.Column(SA.DateTime, nullable=True)
    # 结束日期
    end_date = SA.Column(SA.DateTime, nullable=True)
    # 每个词条最多翻译数 -1 表示无限制
    max_translate_count = SA.Column(SA.Integer, default=-1)
    # 期望完成日期
    completion_date = SA.Column(SA.DateTime, nullable=True)
    # 实际完成日期
    real_completion_date = SA.Column(SA.DateTime, nullable=True)

    #类型
    type = SA.Column(BIGINT(unsigned=True), nullable=True, default=TASK_TYPE_TEXT)

    # group_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('group.id'), nullable=False)

    file_id = SA.Column(BIGINT(unsigned=True), nullable=True)

    content = relationship('CrowdSourceTaskContent', uselist=False, backref='task')

    participators = relationship('CrowdSourceTaskParticipator', backref='task',
                                 order_by="CrowdSourceTaskParticipator.tar_lang, "
                                          "desc(CrowdSourceTaskParticipator.translated_word_count)")

    glossaries = relationship('Glossary', secondary=TaskGlossaryRelTable, backref=backref("task", uselist=False))

    #图片任务backref
    images = relationship('Image', backref='task', order_by="Image.position")

    comments = relationship('CrowdSourceTaskComment', backref='task')
    tag_rel_list = relationship('CrowdSourceTaskTagRel', backref='task', lazy='joined', cascade='delete-orphan, delete')

    def tar_lang_list(self, with_completed=True):
        """
        目标语言列表，
        :param with_completed=True
            是否包含已完成的目标语言
        """
        tar_lang_list = self.tar_lang.split(',') if self.tar_lang else []
        if not with_completed:
            subtract = set(tar_lang_list) - set(self.completed_tar_lang_list)
            return list(subtract)
        return tar_lang_list

    def avatar_url(self, default='literature'):
        task_images = self.task_images()
        if task_images:
            return task_images[0]
        return url_for('static', filename='images/frontend/%s.jpg' % default)

    @property
    def show_expand(self):
        return len(strip_tags(self.task_content)) > 300

    def task_images(self):
        if self.type == self.TASK_TYPE_TEXT:
            return filter_images(self.task_content)
        elif self.type == self.TASK_TYPE_IMAG:
            if self.session:
                return self.images
            else:
                return self.image_list

    def get_creator(self):
        with session_cm() as account_session:
            return account_session.query(Account).get(self.creator_id)

    def task_file(self):
        if not self.file_id:
            return None
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            return db_session.query(File).options(joinedload(File.file_content)).get(self.file_id)

    def is_admin(self, user):
        return (self.group and self.group.is_admin(user)) or self.creator_id == user.id

    def update_task(self, task_name, task_content, status, src_lang, tar_lang, tags_str):
        self.name = task_name
        self.src_lang = src_lang
        self.tar_lang = ','.join(tar_lang)
        self.content.content = task_content

        tags = Tag.update_tags(self.session, tags_str, self.tags)
        tag_rel_list = []
        for tag in tags:
            rel = CrowdSourceTaskTagRel()
            rel.task = self
            rel.tag = tag
            tag_rel_list.append(rel)
        self.tag_rel_list = tag_rel_list
        self.session.commit()
        if status:
            self.active()

    @property
    def time_archive(self):
        return self.created_date.strftime('%Y年%m月')

    @property
    def like_count(self):
        from nowdo.controls.like import LikeRel
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            return self.session.query(count(LikeRel.id)).filter(LikeRel.task_id == self.id).scalar()

    @property
    def task_content(self):
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            if self.content:
                return self.content.content
            task_file = self.task_file()
            if task_file:
                return task_file.file_content.content
            return ""

    @property
    def tags(self):
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            return [rel.tag for rel in self.tag_rel_list]

    @property
    def comment_count(self):
        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            return self.session.query(count(CrowdSourceTaskComment.id))\
                .filter(CrowdSourceTaskComment.task_id == self.id)\
                .scalar()

    @property
    def image_num(self):
        if self.type == self.TASK_TYPE_TEXT:
            return len(self.task_images())
        elif self.type == self.TASK_TYPE_IMAG:
            with session_cm() as db_session:
                task_image_number = db_session.query(Image).filter(Image.task_id == self.id).count()
                return task_image_number

    @property
    def image_list(self):
        with session_cm() as db_session:
            task_image_list = db_session.query(Image).filter(Image.task_id == self.id).order_by(Image.position).all()
            return task_image_list

    @property
    def summery_image_url(self):
        if self.type == self.TASK_TYPE_TEXT:
            task_images = self.task_images()
            return task_images[0] if task_images else None
        elif self.type == self.TASK_TYPE_IMAG:
            with session_cm() as db_session:
                task_image = db_session.query(Image).filter(Image.task_id == self.id)\
                    .order_by(Image.position.asc()).first()
                return task_image.image_url if task_image else None

    @property
    def is_maturity(self):
        if not self.end_date:
            return False
        return datetime.datetime.now() > self.end_date

    @property
    def is_translating(self):
        return self.status == CrowdSourceTask.STATUS_TRANSLATING

    @property
    def is_finished(self):
        return self.status == CrowdSourceTask.STATUS_FINISHED

    @property
    def editable(self):
        return self.status == CrowdSourceTask.STATUS_INIT

    @property
    def completed_tar_lang_list(self):
        return self.completed_tar_lang.split(',') if self.completed_tar_lang else []

    @property
    def reserved_words_list(self):
        return self.reserved_words.replace("，", ",").split(",") if self.reserved_words else None

    @property
    def all_language_translate_progress(self):
        """
        所有语言的翻译进度
        """
        return self.tar_lang_list_with_translate_progress()

    @property
    def task_link(self):
        # if self.is_translating:
        #     return self.read_link()
        # # 所有的任务都先跳转到阅读页面
        # else:
        return url_for('task.task_view', task_id=str(self.id), _external=True)

    def read_link(self, tar_lang=None):
        return self._translate_tool_link('read', tar_lang)

    def translate_link(self, tar_lang=None):
        return self._translate_tool_link('translate', tar_lang)

    def approve_link(self, tar_lang=None):
        return self._translate_tool_link('approve', tar_lang)

    def _translate_tool_link(self, tool_type, tar_lang):
        if tar_lang is None:
            tar_lang = self.tar_lang_list()[0]
        return url_for('task.task_translate', task_id=self.id) + '#%s/%s' % (tool_type, tar_lang)

    @classmethod
    def create_crowd_source_task(cls, session, name, src_lang, languages, status, tags_str,
                                 description=None,
                                 group=None,
                                 content=None,
                                 uploaded_file=None,
                                 # glossary_table_id=None,
                                 max_translate_count=100,
                                 start_date=None, end_date=None,
                                 reserved_words=None
                                 ):

        orig_file = None
        if uploaded_file:
            filename = get_random_filename() + os.path.splitext(uploaded_file.name)[1]
            orig_file = kf.create_orig_file(session, setting.TASK_FILE_GROUP_STR, filename, src_lang, uploaded_file.read())

        crowd_task = cls(name=name,
                         src_lang=src_lang,
                         tar_lang=','.join(languages),
                         file_id=orig_file.id if orig_file else None,
                         entry_count=0,
                         word_count=0,
                         description=description,
                         max_translate_count=max_translate_count,
                         start_date=start_date,
                         end_date=end_date,
                         reserved_words=reserved_words,
                         creator_id=current_user.id,
                         type=cls.TASK_TYPE_TEXT)
        tags = Tag.update_tags(session, tags_str)
        session.add_all(tags)
        task_content = CrowdSourceTaskContent(task=crowd_task, content=deal_task_content(content))
        session.add(task_content)
        if group:
            crowd_task.group = group

        tag_rel_list = []
        for tag in tags:
            rel = CrowdSourceTaskTagRel()
            rel.task = crowd_task
            rel.tag = tag
            tag_rel_list.append(rel)

        crowd_task.tag_rel_list = tag_rel_list
        session.add(crowd_task)

        # if glossary_table_id:
        #     from nowdo.controls.glossary import GlossaryTable
        #     glossary_table = session.query(GlossaryTable).get(glossary_table_id)
        #     crowd_task.glossary_tables = [glossary_table]

        session.commit()

        if status:
            crowd_task.active()

        Trends.add_trends(current_user, TREND_ACTION_CREATE, TREND_TARGET_TYPE_TASK, crowd_task)
        return crowd_task

    @classmethod
    def create_img_task(cls, session, name, src_lang, languages, status, tags_str,
                        img_list=[],
                        description=None,
                        group=None,
                        max_translate_count=100,
                        start_date=None,
                        end_date=None,
                        reserved_words=None):

        crowd_task = cls(name=name,
                         src_lang=src_lang,
                         tar_lang=','.join(languages),
                         file_id=None,
                         entry_count=0,
                         word_count=0,
                         description=description,
                         max_translate_count=max_translate_count,
                         start_date=start_date,
                         end_date=end_date,
                         reserved_words=reserved_words,
                         creator_id=current_user.id,
                         type=cls.TASK_TYPE_IMAG)
        tags = Tag.update_tags(session, tags_str)
        session.add_all(tags)
        if group:
            crowd_task.group = group

        tag_rel_list = []
        for tag in tags:
            rel = CrowdSourceTaskTagRel()
            rel.task = crowd_task
            rel.tag = tag
            tag_rel_list.append(rel)

        crowd_task.tag_rel_list = tag_rel_list
        session.add(crowd_task)

        session.commit()

        if status:
            crowd_task.active()

        for i in xrange(len(img_list)):
            Image.create(session, img_list[i], i, crowd_task.id)

        Trends.add_trends(current_user, TREND_ACTION_CREATE, TREND_TARGET_TYPE_TASK, crowd_task)
        return crowd_task

    @staticmethod
    def tasks_with_my_glossary(db_session, user, page=None, per_page=None):
        task_query = db_session.query(CrowdSourceTask, count())\
            .join(CrowdSourceTask.glossaries)\
            .filter(Glossary.creator_id == user.id)\
            .group_by(CrowdSourceTask.id)\
            .order_by(Glossary.created_date.desc())
        return pagination_or_not(task_query, page, per_page, default_per_page=CrowdSourceTask.PER_PAGE)

    @staticmethod
    def featured_tasks(db_session, tag_name=None, page=None, per_page=None):
        task_query = db_session.query(CrowdSourceTask)\
            .join(CrowdSourceTask.tag_rel_list)\
            .filter(CrowdSourceTaskTagRel.is_featured == True)
        if tag_name:
            tag = Tag.get_by_name(db_session, tag_name)
            task_query = task_query.filter(CrowdSourceTaskTagRel.tag == tag)

        task_query = task_query.order_by(CrowdSourceTask.created_date.desc())
        return pagination_or_not(task_query, page, per_page, default_per_page=CrowdSourceTask.PER_PAGE)

    @staticmethod
    def participated_tasks(db_session, user, page=None, per_page=None):
        participated_task_ids = db_session.query(CrowdSourceTaskParticipator.task_id.distinct()). \
            filter(CrowdSourceTaskParticipator.account_email == user.email).subquery()

        task_query = db_session.query(CrowdSourceTask) \
            .filter(CrowdSourceTask.id.in_(participated_task_ids)) \
            .order_by(CrowdSourceTask.created_date.desc())
        return pagination_or_not(task_query, page=page, per_page=per_page, default_per_page=CrowdSourceTask.PER_PAGE)

    @staticmethod
    def published_tasks(db_session, user, page=None, per_page=None):

        task_query = db_session.query(CrowdSourceTask) \
            .filter(CrowdSourceTask.creator_id == user.id) \
            .order_by(CrowdSourceTask.created_date.desc())
        return pagination_or_not(task_query, page=page, per_page=per_page, default_per_page=CrowdSourceTask.PER_PAGE)

    @staticmethod
    def liked_tasks(db_session, user, page=None, per_page=None):
        from nowdo.controls.like import LikeRel

        task_query = db_session.query(CrowdSourceTask) \
            .join(CrowdSourceTask.like_rel_list)\
            .filter(LikeRel.user_id == user.id) \
            .order_by(LikeRel.created_date.desc())
        return pagination_or_not(task_query, page=page, per_page=per_page, default_per_page=CrowdSourceTask.PER_PAGE)

    @staticmethod
    def tagged_tasks(db_session, tag_name, featured_only=False, page=None, per_page=None):
        """
        打了某个标签的任务列表
        """
        task_query = db_session.query(CrowdSourceTask) \
            .join(CrowdSourceTask.tag_rel_list).join(Tag)

        if featured_only:
            task_query = task_query.filter(CrowdSourceTaskTagRel.is_featured == True)

        if tag_name:
            task_query = task_query.filter(Tag.tag_name == tag_name)

        return pagination_or_not(task_query, page=page, per_page=per_page, default_per_page=CrowdSourceTask.PER_PAGE)

    @staticmethod
    def tagged_tasks_by_id(db_session, tag_ids, featured_only=False, page=None, per_page=None):
        """
        打了某个标签的任务列表
        """
        task_query = db_session.query(CrowdSourceTask) \
            .join(CrowdSourceTask.tag_rel_list).join(Tag)

        if featured_only:
            task_query = task_query.filter(CrowdSourceTaskTagRel.is_featured == True)

        if type(tag_ids) != list:
            tag_ids = list(tag_ids)
            task_query = task_query.filter(Tag.id.in_(tag_ids))

        return pagination_or_not(task_query, page=page, per_page=per_page, default_per_page=CrowdSourceTask.PER_PAGE)

    @classmethod
    def search_by_name(cls, db_session, search_name, max=5):
        query = db_session.query(cls).order_by(cls.created_date.desc())
        if search_name:
            query = query.filter(cls.name.like("%" + search_name + "%"))

        if max:
            query = query.limit(max)

        return query.all()

    def create_glossary(self, user, source, target, lang):
        glossary = Glossary(source=source,
                            target=target,
                            tar_lang=lang,
                            creator_id=user.id)
        self.glossaries.append(glossary)
        self.session.commit()
        return glossary

    def entries(self):
        entry_list = kf.get_word_list(setting.TASK_FILE_GROUP_STR, self.file_id)
        return entry_list

    def tar_lang_list_with_translate_progress(self, with_completed=True):
        """
        带有翻译进度的目标语言列表
        return (tar_lang, translated_entry_count, translated_word_count, translated_word_percent)
        """
        tar_languages = self.tar_lang_list(with_completed)
        lang_progress_list = []
        for tar_lang in tar_languages:
            lang_progress_list.append(self.translate_progress(tar_lang))
        return sorted(lang_progress_list, key=lambda x: x[2], reverse=True)

    def tar_lang_list_with_approve_progress(self, with_completed=True):
        """
        (tar_lang, approved_entry_count, approved_percent)
        """
        tar_languages = self.tar_lang_list(with_completed)
        lang_progress_list = []
        for tar_lang in tar_languages:
            lang_progress_list.append(self.approve_progress(tar_lang))
        return sorted(lang_progress_list, key=lambda x: x[2], reverse=True)

    def latest_results(self, limit=5):
        results = object_session(self).query(CrowdSourceTaskResult). \
            filter(CrowdSourceTaskResult.task_id == self.id). \
            order_by(CrowdSourceTaskResult.created_date.desc()). \
            limit(limit)
        return results

    def redo_translation_for_tar_lang(self, tar_lang):
        """
        1. 将当前语言从已完成语言列表中移除
        2. 修改任务的状态为翻译中（如果已经完成的话）
        """
        completed_tar_lang_list = self.completed_tar_lang_list
        completed_tar_lang_list.remove(tar_lang)
        self.completed_tar_lang = ','.join(completed_tar_lang_list)
        self.status = CrowdSourceTask.STATUS_TRANSLATING
        self.session.commit()

    def end_translation_for_tar_lang(self, tar_lang):
        """
        完成当前任务某语言的翻译
        1. 回写翻译结果
        2. 合成文件
        3. 修改已完成的翻译语言
        """
        trans_entries = kf.get_word_list(setting.TASK_FILE_GROUP_STR, self.file_id)
        trans_results = self.used_results(tar_lang)

        if len(trans_entries) != len(trans_results):
            return False, u'还有未确认翻译结果的词条'

        word_list = [(r.content, r.entry_position) for r in trans_results]

        fill_res = kf.fill_word_list(self.file_id, tar_lang, word_list)
        integrate_res = kf.integrate(self.file_id, tar_lang)

        if fill_res and integrate_res:

            if self.completed_tar_lang:
                self.completed_tar_lang = self.completed_tar_lang + ',' + tar_lang
            else:
                self.completed_tar_lang = tar_lang

            if len(self.completed_tar_lang_list) == len(self.tar_lang_list()):
                self.status = CrowdSourceTask.STATUS_FINISHED
            self.session.commit()
            return True, 'success'
        else:
            return False, u'完成翻译失败'

    def used_results(self, tar_lang):
        cur_lang_results = self.session.query(CrowdSourceTaskResult).filter(CrowdSourceTaskResult.tar_lang == tar_lang,
                                                                            CrowdSourceTaskResult.task_id == self.id,
                                                                            CrowdSourceTaskResult.used == True).all()
        return cur_lang_results

    def showed_results(self, tar_lang):
        """

        :param tar_lang:
        :return:
        1.select * from crowd_source_task_result as a
        where a.modified_date = (
        select max(modified_date) from crowd_source_task_result as b
        where b.entry_id = a.entry_id)
        order by entry_id asc;
        2.SELECT
            *
        FROM
            (
                SELECT
                    *
                FROM
                    crowd_source_task_result
                ORDER BY
                    modified_date DESC
            ) AS a
        GROUP BY
            a.entry_id;
        """
        used_entry_subquery = self.session.query(CrowdSourceTaskResult.entry_id).filter(
            CrowdSourceTaskResult.tar_lang == tar_lang,
            CrowdSourceTaskResult.task_id == self.id,
            CrowdSourceTaskResult.used==True
        ).subquery()

        result_order_subquery = self.session.query(CrowdSourceTaskResult).order_by(
            CrowdSourceTaskResult.modified_date.desc()).subquery()

        result_subquery = self.session.query(result_order_subquery.c.id).filter(
            result_order_subquery.c.tar_lang == tar_lang,
            result_order_subquery.c.task_id == self.id,
            not_(CrowdSourceTaskResult.entry_id.in_(used_entry_subquery))
        ).group_by(result_order_subquery.c.entry_id).subquery()

        cur_lang_results = self.session.query(CrowdSourceTaskResult).filter(
            or_(
                and_(
                    CrowdSourceTaskResult.tar_lang == tar_lang,
                    CrowdSourceTaskResult.task_id == self.id,
                    CrowdSourceTaskResult.used==True
                ),
                CrowdSourceTaskResult.id.in_(result_subquery)
            )
        )

        return cur_lang_results.all()

    def is_active(self):
        return self.status == CrowdSourceTask.STATUS_TRANSLATING

    def create_task_file(self):
        filename = get_random_filename() + '.txt'
        orig_file = kf.create_orig_file(self.session,
                                        setting.TASK_FILE_GROUP_STR,
                                        filename,
                                        self.src_lang, strip_tags(self.task_content))
        self.file_id = orig_file.id
        # 创建文件后立即分解文件
        self.extract_task_file()

    def extract_task_file(self):
        celery.send_task('nowdo.tasks.translate.extract_worker',
                         [setting.TASK_FILE_GROUP_STR, self.file_id, self.tar_lang_list()])
        # from nowdo.tasks.translate import extract_worker
        # extract_worker(setting.TASK_FILE_GROUP_STR, self.file_id, self.tar_lang_list())
        self.session.commit()

    def active(self):
        """
        开启翻译
            1. 如果没有task_file，创建文件，分解词条
            2. 如果有文件，没有词条，重新分解词条
        """
        pre_status = self.status
        self.status = CrowdSourceTask.STATUS_TRANSLATING

        if pre_status == CrowdSourceTask.STATUS_CLOSED:
            self.session.commit()

        if not self.file_id:
            self.create_task_file()
        elif len(self.entries()) <= 0:
            self.extract_task_file()

    def deactivate(self):
        self.status = CrowdSourceTask.STATUS_CLOSED
        self.session.commit()

    def approve_result(self, entry_id, result_id, tar_lang):
        """
        确认翻译结果
        """
        self.session.query(CrowdSourceTaskResult) \
            .filter(CrowdSourceTaskResult.task_id == self.id,
                    CrowdSourceTaskResult.tar_lang == tar_lang,
                    CrowdSourceTaskResult.entry_id == entry_id,
                    CrowdSourceTaskResult.used == True) \
            .update({'used': False}, synchronize_session=False)

        result = self.session.query(CrowdSourceTaskResult).get(result_id)
        result.approve()
        return result

    def cancel_approve_result(self, result_id):
        """
        取消确认翻译结果
        """
        result = self.session.query(CrowdSourceTaskResult).get(result_id)
        result.cancel_approve()
        return result

    def cancel_all_approve_result(self, tar_lang):
        """
        取消确认所有翻译结果
        """
        results = self.session.query(CrowdSourceTaskResult).filter(CrowdSourceTaskResult.tar_lang == tar_lang).all()
        for r in results:
            if r.used:
                r.cancel_approve()

    def has_translate_result(self):
        return self.session.query(CrowdSourceTaskResult).filter(CrowdSourceTaskResult.task_id == self.id).count() > 0

    def translate_progress(self, tar_lang):
        """
            (tar_lang, translated_entry_count, translated_word_count, translated_word_percent)
        """
        translated_entry_count, translated_word_count = self.translated_count(tar_lang)
        if self.word_count == 0:
            translated_word_percent = 0
        else:
            translated_word_percent = float('%0.3f' % (float(translated_word_count)/float(self.word_count))) * 100
        return tar_lang, translated_entry_count, translated_word_count, str(translated_word_percent)

    def approve_progress(self, tar_lang):
        """
            (tar_lang, approved_entry_count, approved_word_count, approved_percent)
        """
        approved_entry_count, approved_word_count = self.approved_count(tar_lang)
        approved_count_percent = float('%0.3f' % (float(approved_word_count)/float(self.word_count))) * 100
        return tar_lang, approved_entry_count, approved_word_count, str(approved_count_percent)

    def translated_count(self, tar_lang):
        translated_word_count = 0
        translated_entry_count = 0

        with session_cm() as db_session:
            if not self.session:
                db_session.add(self)
            translated_entry_ids = self.session.query(CrowdSourceTaskResult.entry_id.distinct()). \
                filter(CrowdSourceTaskResult.task_id == self.id,
                       CrowdSourceTaskResult.tar_lang == tar_lang).all()
            entry_ids = [e[0] for e in translated_entry_ids]
            entries = kf.get_part_entries(setting.TASK_FILE_GROUP_STR, self.file_id, entry_ids)
            if entries:
                translated_word_count = sum([item.word_count for item in entries])
                translated_entry_count = len(entries)

            return translated_entry_count, translated_word_count

    def approved_count(self, tar_lang):

        approved_entry_ids_query = self.session.query(CrowdSourceTaskResult.entry_id.distinct()). \
            filter(CrowdSourceTaskResult.task_id == self.id,
                   CrowdSourceTaskResult.tar_lang == tar_lang,
                   CrowdSourceTaskResult.used == True)

        approved_entry_count = approved_entry_ids_query.count()

        approved_entry_id_list = approved_entry_ids_query.all()
        approved_entry_ids = [e[0] for e in approved_entry_id_list]
        approved_entries = kf.get_part_entries(self.group_id, self.file_id, approved_entry_ids)

        approved_word_count = sum([e.word_cnt for e in approved_entries])

        return approved_entry_count, approved_word_count

    def get_status_str(self):
        if self.status == CrowdSourceTask.STATUS_FINISHED:
            return u'任务完成'
        if self.status == CrowdSourceTask.STATUS_INIT:
            return u'未启用'
        if self.is_translating:
            return u'众包翻译中'
        return u'已开启'

    def is_translate_finished(self, tar_lang):
        return tar_lang in self.completed_tar_lang_list

    def to_dict(self, with_progress=False, with_completed=True):
        ret = {
            'id': str(self.id),
            'name': self.name,
            'creator_id': self.creator_id,
            'group': self.group.to_dict() if self.group else None,
            'src_lang': self.src_lang,
            'tar_lang_list': self.tar_lang_list(with_completed),
            'completed_lang_list': self.completed_tar_lang_list,
            'word_count': self.word_count,
            'entry_count': self.entry_count,
            'description': self.description,
            'status': self.status,
            'is_maturity': self.is_maturity,
            'status_human': self.get_status_str(),
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'max_translate_count': self.max_translate_count,
            'participator_count': len(self.participators),
            'language_count': len(self.tar_lang_list()),
            'task_link': self.task_link,
            'task_images': self.task_images(),
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M'),
            'type': self.type,
        }
        if with_progress:
            ret.update(tar_lang_list_with_progress=self.tar_lang_list_with_translate_progress(with_completed))
        return ret


class CrowdSourceTaskParticipator(Base):
    """
    主题参与者的统计信息
    """
    __tablename__ = 'crowd_source_task_participator'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)

    PER_PAGE = 30

    #: 任务 ID
    task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id'), nullable=False)
    #: 用户 ID
    account_email = SA.Column(String(128), index=True, nullable=False)
    # 目标语言
    tar_lang = SA.Column(SA.String(4), nullable=False)
    # 翻译词条量
    translated_entry_count = SA.Column(SA.Integer, default=0)
    # 翻译单词量
    translated_word_count = SA.Column(SA.Integer, default=0)
    # 采纳的词条量
    approved_entry_count = SA.Column(SA.Integer, default=0)
    # 采纳的单词量
    approved_word_count = SA.Column(SA.Integer, default=0)
    # 点赞数
    praise_count = SA.Column(SA.Integer, default=0)

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.account_email,
            'translated_entry_count': self.translated_entry_count,
            'translated_word_count': self.translated_word_count,
            'tar_lang': self.tar_lang,
            'approved_entry_count': self.approved_entry_count,
            'approved_word_count': self.approved_word_count,
            'approved_percent': str(float('%0.3f' %
                                          float(float(self.approved_word_count)/float(self.translated_word_count))) * 100)
        }

    @classmethod
    def get_or_create(cls, db_session, task_id, tar_lang, account_email):
        participator = db_session.query(CrowdSourceTaskParticipator). \
            filter(CrowdSourceTaskParticipator.task_id == task_id,
                   CrowdSourceTaskParticipator.tar_lang == tar_lang,
                   CrowdSourceTaskParticipator.account_email == account_email).first()

        if not participator:
            participator = CrowdSourceTaskParticipator(task_id=task_id,
                                                       account_email=current_user.email,
                                                       tar_lang=tar_lang)
            db_session.add(participator)

            ## 记录参与任务动态
            # task = db_session.query(CrowdSourceTask).get(task_id)
            # Trends.add_trends(current_user, TREND_ACTION_PARTICIPATE, TREND_TARGET_TYPE_TASK, task)
        return participator

    @classmethod
    def billboard(cls, session, order_by='translated_word_sum desc', limit=10):
        rank_list = session.query(CrowdSourceTaskParticipator.account_email,
                                  count(CrowdSourceTaskParticipator.task_id.distinct()),
                                  count(CrowdSourceTaskParticipator.tar_lang.distinct()),
                                  sa_sum(CrowdSourceTaskParticipator.translated_word_count).label('translated_word_sum'),
                                  sa_sum(CrowdSourceTaskParticipator.approved_word_count).label('approved_word_sum'),
                                  sa_sum(CrowdSourceTaskParticipator.praise_count).label('praise_count_sum')) \
            .group_by(CrowdSourceTaskParticipator.account_email) \
            .order_by(order_by) \
            .limit(limit).all()
        return rank_list

    @classmethod
    def personal_statistic(cls, db_session, group, email):
        task_ids = [t.id for t in group.tasks]

        participated_task_count, participated_language_count, translated_word_count, used_word_count, praise_count_sum = \
            db_session.query(count(CrowdSourceTaskParticipator.task_id.distinct()),
                             count(CrowdSourceTaskParticipator.tar_lang.distinct()),
                             sa_sum(CrowdSourceTaskParticipator.translated_word_count),
                             sa_sum(CrowdSourceTaskParticipator.approved_word_count),
                             sa_sum(CrowdSourceTaskParticipator.praise_count)) \
                .filter(CrowdSourceTaskParticipator.account_email == email,
                        CrowdSourceTaskParticipator.task_id.in_(task_ids)).first()

        return {
            'participated_task_count': participated_task_count,
            'participated_language_count': participated_language_count,
            'translated_word_count': translated_word_count or 0,
            'used_word_count': used_word_count or 0,
            'praise_count_sum': praise_count_sum or 0
        }


class CrowdSourceTaskResult(Base):
    """
    翻译结果表
    """
    __tablename__ = 'crowd_source_task_result'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)

    PER_PAGE = 30

    #: 任务 ID
    task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id'), nullable=False)
    #: entry id
    entry_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    #: 词条位置
    entry_position = SA.Column(BIGINT(unsigned=True), nullable=False)
    #: 目标语言
    tar_lang = SA.Column(SA.String(4), index=True)
    #: 内容
    content = SA.Column(SA.Text, nullable=False)
    # 翻译人
    translator = SA.Column(SA.String(255), index=True, nullable=True)
    # 是否使用
    used = SA.Column(SA.Boolean, default=False)

    comments = SA.Column(SA.Text)

    voters = relationship('CrowdSourceTaskResultVote', backref='result')
    # entry = relationship('Entry')
    task = relationship('CrowdSourceTask')

    @property
    def translator_display_name(self):
        from nowdo.controls.account import Account
        with session_cm() as account_session:
            user = account_session.query(Account).filter_by(email=self.translator).one()
            translator = user.display_name and user.display_name or self.translator
            return translator

    @classmethod
    def add_result(cls, db_session, task_id, entry_id, entry_position, tar_lang, target_text):
        """
        1. 查看当前用户是否参与过该任务
            1）没有：添加一条参与者记录
            2）有：pass
        2. 查看当前用户对当前词条有无翻译结果
            1）没有：增加一条翻译结果
            2）有：更新翻译结果
        3. 更新参与者翻译量
        """
        participator = CrowdSourceTaskParticipator.get_or_create(db_session, task_id, tar_lang, current_user.email)

        trans_result = db_session.query(CrowdSourceTaskResult). \
            filter(CrowdSourceTaskResult.task_id == task_id,
                   CrowdSourceTaskResult.entry_id == entry_id,
                   CrowdSourceTaskResult.tar_lang == tar_lang,
                   CrowdSourceTaskResult.translator == current_user.email).first()

        if not trans_result:

            trans_result = CrowdSourceTaskResult(task_id=task_id, entry_id=entry_id, entry_position=entry_position,
                                                 tar_lang=tar_lang, translator=current_user.email, content=target_text)
            task = db_session.query(CrowdSourceTask).get(task_id)
            participator.translated_entry_count += 1
            entry = kf.get_part_entries(setting.TASK_FILE_GROUP_STR, task.file_id, [entry_id])
            if entry:
                word_cnt = entry[0].word_count
                participator.translated_word_count += word_cnt
        else:
            if trans_result.used:
                return False, u'该翻译结果已经被确认'
            trans_result.content = target_text
        db_session.add(trans_result)
        db_session.commit()
        return True, trans_result

    def get_participator(self):
        return self.session.query(CrowdSourceTaskParticipator) \
            .filter(CrowdSourceTaskParticipator.account_email == self.translator,
                    CrowdSourceTaskParticipator.task_id == self.task_id,
                    CrowdSourceTaskParticipator.tar_lang == self.tar_lang).one()

    def vote_count(self):
        # return self.session.query(CrowdSourceTaskResultVote).filter_by(result_id=self.id).count()
        return len(self.voters)

    def voted_by(self, voter):
        return self.session.query(CrowdSourceTaskResultVote).filter_by(result_id=self.id, voter=voter).count() > 0

    def vote(self, delete_on_existed=True):
        participator = self.get_participator()
        vote = self.session.query(CrowdSourceTaskResultVote). \
            filter(CrowdSourceTaskResultVote.result_id == self.id,
                   CrowdSourceTaskResultVote.voter == current_user.email).first()
        if vote:
            if delete_on_existed:
                self.session.delete(vote)
                if participator.praise_count > 0:
                    participator.praise_count -= 1
        else:
            vote = CrowdSourceTaskResultVote(result_id=self.id, voter=current_user.email)
            self.session.add(vote)
            if not participator.praise_count:
                participator.praise_count = 0
            participator.praise_count += 1
        self.session.commit()

    def to_dict(self):

        return {
            'id': str(self.id),
            'content': self.content,
            'email': self.translator,
            'translator': self.translator_display_name,
            'tar_lang': self.tar_lang,
            'used': self.used,
            'vote_count': self.vote_count(),
            'created_date_delta': date_delta(self.created_date),
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'modified_date_delta': date_delta(self.modified_date),
            'modified_date': self.modified_date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def entry(self):
        entries = kf.get_part_entries(setting.AVATAR_FILE_GROUP_STR, self.task.file_id, [self.entry_id])
        if entries and len(entries) > 0:
            return entries[0]
        else:
            return None

    def approve(self):
        self.used = True
        # 修改采纳量
        participator = self.get_participator()
        participator.approved_entry_count += 1
        participator.approved_word_count += self.entry().word_count

    def cancel_approve(self):
        self.used = False
        # 修改采纳量
        participator = self.get_participator()
        participator.approved_entry_count -= 1
        participator.approved_word_count -= self.entry().word_count


class CrowdSourceTaskResultVote(Base):
    __tablename__ = 'crowd_source_task_result_vote'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)

    result_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task_result.id'), nullable=False)
    voter = SA.Column(SA.String(255), index=True, nullable=True)


class CrowdSourceTaskComment(Base):
    """
    主题评论表
    """
    PER_PAGE = 30
    __tablename__ = 'crowd_source_task_comment'

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)

    task_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('crowd_source_task.id'), nullable=False)
    creator_id = SA.Column(BIGINT(unsigned=True), nullable=False)
    content = SA.Column(SA.TEXT)

    @property
    def creator(self):
        with session_cm() as account_session:
            return account_session.query(Account).get(self.creator_id)

    @staticmethod
    def create_comment(db_session, task, content):
        comment = CrowdSourceTaskComment(task=task, content=content, creator_id=current_user.id)
        db_session.add(comment)
        db_session.commit()
        # Trends.add_trends(current_user, TREND_ACTION_REPLY, TREND_TARGET_TYPE_TASK, task)
        Notice.create(db_session, Notice.NOTICE_TYPE_COMMENT, current_user.id, task.creator_id, comment.id)
        return comment

    @staticmethod
    def get_comments(db_session, task_id, page=None, per_page=None):
        comment_query = db_session.query(CrowdSourceTaskComment)\
            .filter(CrowdSourceTaskComment.task_id == task_id).order_by(CrowdSourceTaskComment.created_date.desc())
        return pagination_or_not(comment_query, page=page, per_page=per_page, default_per_page=CrowdSourceTaskComment.PER_PAGE)