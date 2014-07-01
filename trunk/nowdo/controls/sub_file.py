#coding=utf8
from sqlalchemy.orm import object_session
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT, BINARY
from sqlalchemy import Index, Table, MetaData

from kfile.controls.base import Base, id_generate, file_db


def dynamic_file(tablename, mysql_engine="MyISAM"):
    class SubFile(Base):
        ###################################################################
        # MyISAM Table, 必须和File表（merge表）结构保持一致!!!
        __tablename__ = tablename
        __table_args__ = (
                          {"mysql_charset": "utf8", "mysql_engine": mysql_engine})

        PER_PAGE = 30

        session = property(lambda self: object_session(self))
        PER_PAGE = 30

        id = SA.Column(BIGINT(unsigned=True),default=id_generate, primary_key=True)
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

        # 扩展名 到 文件处理器 的dict
        _file_handlers_by_ext = {}

        # content-type 到 文件处理器 的dict
        _file_handlers_by_content_type = {}

        def __init__(self, id, status, source):
            self.id = id
            self.status = status
            self.source = source

    return SubFile