# -*- coding: utf-8 -*-
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.base import Base, id_generate

__author__ = 'lhfu'


class FileContent(Base):

    ###################################################################
    # merge Table, 必须和dynamic_file中的sub_file表（merge的子表）结构保持一致!!!

    __tablename__ = 'file_content'
    # __table_args__ = {"mysql_charset": "utf8", "mysql_engine": "MERGE"}

    # session = property(lambda self: object_session(self))

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    # #: 文件状态
    # status = SA.Column(SA.SmallInteger)
    # #: 版本号
    # version_no = SA.Column(SA.Integer, default=0)
    # #: 文件类型
    # content_type = SA.Column(SA.String(64))
    # #: 是否dirty，dirty的文件要重新生成
    # dirty = SA.Column(SA.Boolean, default=False)
    # #: 文件内容是否经过gzip压缩
    # gzipped = SA.Column(SA.Boolean, default=False)
    #: 文件内容
    content = SA.Column(SA.Text, nullable=True)
    #: 关联文件id
    file_id = SA.Column(BIGINT(unsigned=True), SA.ForeignKey('file.id'), nullable=False)

    @classmethod
    def create(cls, session, file, content):
        """
        创建文件内容。
        只有orig_file有content。
        每个orig_file只有一个。
        :param session:
        :param file:
        :param content:
        :return:
        """
        ret = cls(content=content, file_id=file.id)

        session.add(ret)
        session.commit()
        return ret

