# -*- coding: utf-8 -*-
import mimetypes
import traceback
from nowdo.controls.file_content import FileContent

try:
    import ujson as json
except ImportError:
    import json

import requests
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT, BINARY
from sqlalchemy.orm import object_session, relationship
from nowdo import setting
from nowdo.utils.session import session_cm, get_main_session
# from kfile.config.celeryconfig import celery

from nowdo.controls.base import Base, id_generate

from kfile.utils.file_parse import get_name_md5
from kfile.utils.gzip_util import gzip_compress
from kfile.utils.krpath import get_ext
from kfile.utils.md5_util import get_md5, get_hex_md5
from nowdo.utils.nowdo_logger import nowdo_logger as logger


str_union = r"(UNION|union)=\(([\d\D]*)\)"

class FileStatus(object):

    DOWNLOADING = 0             # 正在下载
    WAITING_FOR_HANDLING = 1    # 等待分解
    WAITING_FOR_TRANSLATION = 2 # 等待翻译
    MACHINE_COMPLETE = 3        # 机器翻译完成
    NOT_SUPPORTED = 4           # 不支持
    NO_WORD = 5                 # 无词汇
    DELETING = 6                # 正在删除

    FORMAT_EXCEPTION = 20       # 文件内容格式错误
    SWF_EXTRACT_EXCEPTION = 51  # SWF文件分解异常

# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~````````````"
# print len(Base.metadata.sorted_tables)
# print
class FileHandler(object):

    word_handler = None
    supported = None
    ext = None
    content_type = None

    def __init__(self, base_file=None):
        self.base_file = base_file

    def extract(self, content):
        """
        content: 文件内容
        分解文件。返回分解得到的文件扩展名和文件内容字典。
        """
        return {}

    def integrate(self, local_aux_file_dict):
        """
        返回合并后的文件的内容
        """
        return None


class UnsupportedFileHandler(FileHandler):

    supported = False


# session = get_main_session()
class File(Base):

    ###################################################################
    # merge Table, 必须和dynamic_file中的sub_file表（merge的子表）结构保持一致!!!

    __tablename__ = 'file'
    # __table_args__ = {"mysql_charset": "utf8", "mysql_engine": "MERGE"}

    # session = session
    # session = property(lambda self: object_session(self))
    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    #: 文件状态
    status = SA.Column(SA.SmallInteger)
    #: 版本号
    version_no = SA.Column(SA.Integer, default=0)
    #: 文件类型
    content_type = SA.Column(SA.String(64))
    #: 是否dirty，dirty的文件要重新生成
    dirty = SA.Column(SA.Boolean, default=False)
    #: 文件内容是否经过gzip压缩
    gzipped = SA.Column(SA.Boolean, default=False)

    #：文件的来源，域名+相对路径+参数, 不带项目名和语言. complfile的source与其所属origfile的source相同
    source = SA.Column(SA.String(2048))

    #: md5值：group_name + lang + source的md5值
    key = SA.Column(BINARY(16), nullable=False)

    parent_file_id = SA.Column(BIGINT(unsigned=True))

    #: 语言
    lang = SA.Column(SA.String(2), nullable=False)
    #
    group_name = SA.Column(SA.String(64), nullable=False)

    #: 词条数
    count = SA.Column(SA.Integer, default=0)

    REPULL, UPLOAD_FROM_LOCAL, UPLOAD_FROM_SVN = range(3)
    source_type = SA.Column(SA.SmallInteger, default=REPULL)

    #：文件的来源路径md5. complfile与其所属origfile相同
    source_path_md5 = SA.Column(SA.String(64))
    #：文件的来源参数md5. complfile与其所属origfile相同
    source_params_md5 = SA.Column(SA.String(64))

    #relationship
    file_content = relationship("FileContent", backref='file', uselist=False)

    # 扩展名 到 文件处理器 的dict
    _file_handlers_by_ext = {}

    # content-type 到 文件处理器 的dict
    _file_handlers_by_content_type = {}

    def __unicode__(self):
        return u"<File: gridfs_path=%s>" % self.gridfs_path

    def __init__(self, source, lang, group_name):
        self.source = source
        self.lang = lang
        self.group_name = group_name

    @classmethod
    def create(cls, session, group_name, source, lang, parent_file_id=None, **kwargs):
        gridfs_path = '/'.join([group_name, lang, source])
        logger.debug("creating kfile: gridfs_path=%s" %gridfs_path)
        ret = cls(source=source, lang=lang, group_name=group_name)
        for k, v in kwargs.items():
            if k in ('key', 'status', 'content'):
                continue
            setattr(ret, k, v)

        ret.key = get_md5(gridfs_path)
        ret.parent_file_id = parent_file_id
        ret.status = FileStatus.WAITING_FOR_HANDLING
        if ret.params:
            ret.source_params_md5 = get_hex_md5(ret.params)
        ret.source_path_md5 = get_hex_md5(ret.source_without_params)

        session.add(ret)
        session.commit()
        print "source=", ret.source
        return ret

    @classmethod
    def register_file_handler(cls, file_handler_cls_list):
        for file_handler_cls in file_handler_cls_list:
            if getattr(file_handler_cls, 'ext'):
                cls._file_handlers_by_ext[file_handler_cls.ext] = file_handler_cls
            if getattr(file_handler_cls, 'content_type'):
                cls._file_handlers_by_content_type[file_handler_cls.content_type] = file_handler_cls


    def __get_file_handler_instance(self, filename, content_type=None):

        ext = get_ext(filename)
        file_handler_cls = self._file_handlers_by_ext.get(ext, None)
        if file_handler_cls is not None:
            return file_handler_cls(base_file=self)

        if content_type is not None:
            file_handler_cls = self._file_handlers_by_content_type.get(content_type, None)
            if file_handler_cls is not None:
                return file_handler_cls(base_file=self)

        return UnsupportedFileHandler()

    def get_handler(self):
        if not hasattr(self, '__handler'):
            self.__handler = self.__get_file_handler_instance(self.source_without_params,
                self.content_type)
        return self.__handler

    @classmethod
    def delete_multi_by_names(cls, group_name, sources, **kwargs):
        if not sources:
            return
        logger.debug("delete kfile(service:%s ) %s records by: %s" % (group_name, len(sources), "\n".join(sources)))
        with session_cm() as session:
            for src in sources:
                source_path_md5, source_params_md5 = get_name_md5(src)
                files = session.query(File).filter(File.group_name == group_name).\
                    filter(File.source_path_md5 == source_path_md5, File.source_params_md5 == source_params_md5).all()

                filenames = ["/".join([f.group_name, f.lang, f.source]) for f in files]
                logger.warn("%s\n md5=%s" % (source_path_md5, source_params_md5))
                session.query(File).filter(File.group_name == group_name).\
                    filter(File.source_path_md5 == source_path_md5, File.source_params_md5 == source_params_md5).\
                    delete(synchronize_session=False)
                session.commit()
                data = {"filename": filenames}
                requests.post(setting["DNFS_DELETE_FILE"], data)

    @classmethod
    def delete_multi_by_ids(cls, group_name, file_ids, **kwargs):
        """
        : file_ids : a list of file ids
        """
        if not file_ids:
            return

        with session_cm() as session:
            Max = 1000
            start = 0
            end = len(file_ids)

            while start < end:
                files = session.query(File).filter(File.group_name == group_name).\
                    filter(File.id.in_(file_ids[start:start + Max])).all()
                filenames = ["/".join([f.group_name, f.lang, f.source]) for f in files]
                session.query(File).filter(File.group_name==group_name).\
                    filter(File.id.in_(file_ids[start:start + Max])).\
                    delete(synchronize_session=False)
                session.commit()
                data = {"filename": filenames}
                requests.post(setting["DNFS_DELETE_FILE"], data)
                start += Max

    handler = property(get_handler)

    @property
    def path(self):
        return '/'.join([self.group_name, self.lang, self.source])

    @property
    def content(self):
        try:
            # data = {"filename": self.path}
            # ret = requests.post(setting.DNFS_GET_CONTENT, data)
            with session_cm() as db_session:
                if not self.session:
                    db_session.add(self)
                ret = self.session.query(FileContent).filter(FileContent.file_id == self.id).one()
                return ret.content
        except Exception, e:
            print traceback.format_exc()
            print e
            logger.error("get file %s content error" % self.path)
            return ""

    @property
    def params(self):
        a = self.source.split('?')
        if len(a) > 1:
            return '?' + a[1]
        else:
            return ''

    @property
    def gridfs_path(self):
        return '/'.join([self.group_name, self.lang, self.source])


    @property
    def gridfs_path_without_params(self):
        return '/'.join([self.group_name, self.lang, self.source_without_params])


    @property
    def source_without_params(self):
        # return self.source.rsplit('?', 1)[0]
        return self.source.partition('?')[0]

    @property
    def accessible_content_type(self):
        if self.content_type:
            return self.content_type

        guess_content_type = mimetypes.guess_type(self.source_without_params, strict=False)[0]
        if guess_content_type:
            self.update_content_type(guess_content_type)
            return guess_content_type

        return None

    def update_content_type(self, content_type):
        self.content_type = content_type
        self.session.commit()

    @classmethod
    def change_content(cls, group_name, source, lang, content, response_header=None, use_gzip=False):
        with session_cm() as session:
            source_path_md5, source_params_md5 = get_name_md5(source)
            f = session.query(File).filter_by(group_name=group_name,
                                                source_path_md5=source_path_md5,
                                                source_params_md5=source_params_md5,
                                                lang=lang).first()
            logger.debug("update kfile (%s, %s, lang)content(len=%s)" % (source_path_md5, source_params_md5, len(content)))

            if f:
                f.update_content(content, response_header, use_gzip)

    def update_content(self, content, response_header=None, use_gzip=False):
        kwargs = {}
        if use_gzip:
            kwargs['gzipped'] = True
            content = gzip_compress(content)
            self.gzipped = True
            self.session.commit()

        if response_header is not None:
            kwargs['response_header'] = response_header

        kwargs['content_type'] = self.accessible_content_type

        # data = {
        #     "filename": self.path,
        #     "content": content,
        #     "info": json.dumps(kwargs),
        # }
        # requests.post(setting.DNFS_SET_CONTENT, data)
        # fs.update_content(self.gridfs_path, content, kwargs)
        ret = self.session.query(FileContent).filter(FileContent.file_id == self.id).first()
        if ret:
            ret.content = content
            self.session.commit()
        else:
            FileContent.create(self.session, self, content)
        self.incr_version_no()

    def update_count(self, count):
        self.count = count
        self.session.commit()
        print self.id, self.count

    def incr_version_no(self):
        self.version_no += 1
        self.session.commit()
        # self.notify_webproxy('add', {self.source: self.__version_no_with_ctime()})

    @classmethod
    def get_file_by_source_and_lang(cls, session, source, lang, group_name):
        key = get_md5('/'.join([group_name, lang, source]))
        return session.query(File).filter(File.key==key).filter(File.group_name==group_name).first()

    def update_status(self, file_status):
        self.status = file_status
        self.session.commit()

    @property
    def is_js(self):
        if (self.content_type is not None and "javascript" in self.content_type.lower()) or (self.ext == "js"):
            return True

        return False

    @property
    def ext(self):
        return get_ext(self.source_without_params).lower()

    @classmethod
    def register_file_impl(cls, file_impl):
        cls._file_impl = file_impl

    def get_file_impl(self):
        if not hasattr(self, '__file_impl'):
            self.__file_impl = self._file_impl(self)
        return self.__file_impl

    file_impl = property(get_file_impl)

    @property
    def compl_files(self):
        return self.file_impl.compl_files

    def create_compl_files(self, tar_langs):
        return self.file_impl.create_compl_files(tar_langs)

    def get_compl_file_by_lang(self, tar_lang):
        return self.file_impl.get_compl_file_by_lang(tar_lang)


    def extract(self, **kwargs):
        return self.file_impl.extract(**kwargs)

    def integrate(self, orig_file):
        return self.file_impl.integrate(orig_file)

    def insert_word_list(self, word_list):
        self.file_impl.insert_word_list(word_list)