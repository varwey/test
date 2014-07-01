#coding=utf8

import traceback
import sqlalchemy as SA
from sqlalchemy import BINARY, MetaData, Table, Index
from sqlalchemy.dialects.mysql.base import BIGINT
from sqlalchemy.orm import object_session
from Libs.strs.word_cnt import word_cnt
from nowdo.controls.base import Base, id_generate
from kfile.translation.word.word import Word
from kfile.utils.paginator import SQLAlchemyPaginator
from kfile.utils.coding_util import get_unicode, str2utf8
from kfile.utils.kfile_logging import logger
from kfile.utils.md5_util import get_md5
from nowdo.utils.session import session_cm


class Entry(Base):

        ###################################################################
        # merge Table, 必须和dynamic_file中的sub_file表（merge的子表）结构保持一致!!!

        __tablename__ = "entry"
        # __table_args__ = {"mysql_charset": "utf8", "mysql_engine": "InnoDB"}
        PER_PAGE = 30

        id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
        key = SA.Column(BINARY(16), nullable=False)
        word = SA.Column(SA.Text, nullable=False)
        length = SA.Column(SA.SmallInteger)
        weight = SA.Column(SA.SmallInteger)
        description = SA.Column(SA.Text)
        glossary = SA.Column(SA.Boolean, default=False)     #术语/非术语
        content_type = SA.Column(SA.String(64))             #词条类型
        is_enabled = SA.Column(SA.Boolean, default=True)
        human = SA.Column(SA.Boolean, default=False)        #是否要人工翻译
        machine = SA.Column(SA.Boolean, default=True)      #是否要机器翻译
        crowd = SA.Column(SA.Boolean, default=False)        #是否要众包翻译
        group_name = SA.Column(SA.String(64), nullable=False, index=True)
        file_id = SA.Column(BIGINT(unsigned=True), index=True)
        parent_entry_id = SA.Column(BIGINT(unsigned=True))
        is_xc_word = SA.Column(SA.Boolean, default=False, index=True)  # 是否通过add_src_word 和界面上传
        position = SA.Column(BIGINT(unsigned=True))

        # content_type列的可选值
        ENTRY_PLAIN = "text/plain"
        ENTRY_JSON = "text/json"
        ENTRY_XML = "text/xml"

        @staticmethod
        def _calculate_words(s, encoding='utf-8'):
            import re
            from types import StringType

            # RX = re.compile(u"[a-zA-Z0-9_\u0392-\u03c9]+|[\u4E00-\u9FFF\u3400-\u4dbf\uf900-\ufaff\u3040-\u309f\uac00-\ud7af]+", re.UNICODE)
            RX = re.compile(u"[a-zA-Z0-9_\u0392-\u03c9]+|[\u4E00-\u9FFF]+", re.UNICODE)

            if type(s) is StringType:
                s = unicode(s, encoding, 'ignore')

            splitted = RX.findall(s)

            CJK_count = 0
            ASC_count = 0

            for word in splitted:
                if ord(word[0]) >= 12352:   # \u3040
                    CJK_count += len(word)
                else:
                    ASC_count += len(word)

            return CJK_count, ASC_count

        def __init__(self, **kwargs):
            for k, w in kwargs.items():
                if k in ('key', 'length', 'weight', 'content_type'):
                    continue
                setattr(self, k, w)

            if  getattr(self, 'word', None):
                self.key = get_md5(self.word)
                self.length = len(self.word)
                # self.weight = self._calculate_words(self.word)[0]
                self.content_type = self.entry_type

        @classmethod
        def get_part_entries(cls, file_id, entry_id_list):
            with session_cm() as session:
                return session.query(Entry).filter(Entry.file_id==file_id).\
                    filter(Entry.id.in_(entry_id_list)).all()


        @classmethod
        def get_entries_by_file(cls, file_id, group_name):
            with session_cm() as session:
                return session.query(Entry).filter(Entry.file_id== file_id).\
                    filter(Entry.group_name==group_name).order_by(Entry.position).all()
                # exist_entries = session.query(Entry).filter(Entry.file_id== file_id).\
                #     filter(Entry.group_name==group_name).order_by(Entry.position).all()
                # return [(entry.word, entry.position) for entry in exist_entries]

        @classmethod
        def get_entries(cls, group_name, file_id, order='', offset=0, limit=20):
            with session_cm() as session:
                ORDER_METHODS = {
                    '+length': Entry.length.desc(),
                    '-length': Entry.length,
                    '+weight': Entry.weight.desc(),
                    '-weight': Entry.weight,
                    '+string': Entry.word.desc(),
                    '-string': Entry.word,
                    '+modification': Entry.modified_date.desc(),
                    '-modification': Entry.modified_date,
                    '+position': Entry.position.desc(),
                    '-position': Entry.position,
                }
                order = ORDER_METHODS.get(order, None)

                entries = session.query(Entry) \
                    .filter(Entry.group_name == group_name) \
                    .filter(Entry.file_id == file_id) \
                    .order_by(order).offset(offset).limit(limit).all()
                return  entries

        @classmethod
        def create_multi(cls, new_entries_pos, file_id, group_name):
            """
            创建词条，尝试3次
            :param new_entries_pos:  a list of word tuple, such as [(word1, postion1), (word2, postion2)]
            :param group_name:
            :return: 词条id数组，包括已存在的和新创建的
            """
            # print 'ooo', new_entries_pos, file_id
            new_entries_pos = [(str2utf8(word)[0], pos) for word,pos in new_entries_pos]
            with session_cm() as session:
                times = 3
                while times > 0:
                    exist_entries = cls.get_entries_by_file(file_id, group_name)
                    exist_entries_pos = [(entry.word, entry.position) for entry in exist_entries]
                    del exist_entries
                    add_entries_pos = []
                    if set(exist_entries_pos) - set(new_entries_pos):   #如果原词汇顺序有变化,则删除源词条，插入新词条
                        session.query(Entry).filter(Entry.file_id== file_id).\
                            filter(Entry.group_name==group_name).delete(synchronize_session=False)
                        add_entries_pos = new_entries_pos
                    else:                                 #插入新加的词条
                        add_entries_pos = list(set(new_entries_pos) - set(exist_entries_pos))
                    new_entries= []
                    for new_word in add_entries_pos:
                        new_entry = cls(word=new_word[0], position=new_word[1], file_id=file_id, group_name=group_name)
                        new_entries.append(new_entry)
                    session.add_all(new_entries)
                    try:
                        session.commit()
                        return True
                    except Exception, e:
                        session.rollback()
                        logger.error(traceback.format_exc(e))
                        times -= 1

        @classmethod
        def del_multi(cls, file_id, **kwargs):
            try:
                with session_cm() as session:
                    session.query(Entry).filter(Entry.file_id==file_id).delete(synchronize_session=False)
                    session.commit()

                    return True
            except Exception, e:
                session.rollback()
                print traceback.format_exc(e)
                logger.error(traceback.format_exc(e))
                return False

        @classmethod
        def update_entry(self, file_id, group_name, word_list):
            try:
                with session_cm() as session:
                    for item in word_list:
                        entry = session.query(Entry) \
                            .filter(Entry.file_id == file_id) \
                            .filter(Entry.position == item[1]).first()
                        if entry:
                            session.delete(entry)
                            # entry.word = item[0]
                        new_entry = self(word=str2utf8(item[0])[0], position=item[1], file_id=file_id, group_name=group_name)
                        session.add(new_entry)
                    session.commit()
                    return True
            except Exception, e:
                session.rollback()
                print traceback.format_exc(e)
                logger.error(traceback.format_exc(e))
                return False

        @property
        def word_count(self):
            return word_cnt(self.word)

        @property
        def entry_type(self):
            """
            Entry的类型
            :return:
            """
            ret = Entry.ENTRY_PLAIN

            word_type = Word(self.word).type
            if word_type == Word.WORD_JSON:
                ret = Entry.ENTRY_JSON
            elif word_type == Word.WORD_XML:
                ret = Entry.ENTRY_XML

            return ret