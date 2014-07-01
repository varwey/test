# coding=utf-8
"""
created by SL on 14-4-1
"""
import hashlib
import traceback
from bson.objectid import ObjectId
from sqlalchemy.exc import ResourceClosedError, OperationalError
from gridfs import GridFS
from gridfs.errors import NoFile, CorruptGridFile, FileExists
from pymongo import ReadPreference, ReplicaSetConnection, Connection
from pymongo.errors import DuplicateKeyError
from nowdo.config import setting
from nowdo.utils.nowdo_logger import nowdo_logger as logger

__author__ = 'SL'

# coding=utf8


class MetaKey(object):

    RESPONSE_HEADER = "response_header"
    CONTENT_TYPE = "content_type"
    GZIPPED = "gzipped"


class FSHelper(object):
    def get_content(self, filename):
        pass

    def update_content(self, filename, content, **kwargs):
        pass

    def get_md5(self, filename):
        pass

    def get_length(self, filename):
        pass

    def delete(self, filename):
        pass


class GridFSHelper(FSHelper):
    REPLICA_SET_CONN = 0
    MASTER_SLAVE_CONN = 1
    NORMAL_CONN = 2

    def __init__(self, uri, db_name, conn_type):
        if conn_type == GridFSHelper.REPLICA_SET_CONN:
            # 文件系统读写分离，很可能导致文件翻译过程中出错
            self.conn = ReplicaSetConnection(uri, read_preference=ReadPreference.PRIMARY)
        elif conn_type == GridFSHelper.NORMAL_CONN:
            self.conn = Connection(uri)
        else:
            raise Exception("CONNECTION TYPE(%s) NOT SUPPORTED" % conn_type)

        self.db = self.conn[db_name]
        self.files = self.db.fs.files       # fs.files collection
        self.gfs = GridFS(self.db)

    def __get_grid_out(self, object_id):
        """get GridOut object
        """
        try:
            return self.gfs.get(object_id)
        except NoFile:
            # should not get here unless be deleted under concurrent situation
            logger.warn("No content found for object_id: %s" % object_id)

    def get_content(self, object_id):
        """get file content
        """
        grid_out = self.__get_grid_out(object_id)
        if grid_out is not None:
            try:
                return grid_out.read()
            except CorruptGridFile:
                logger.warn(traceback.format_exc())
        return ""

    def get_md5(self, object_id):
        """get file md5
        """
        grid_out = self.__get_grid_out(object_id)
        if grid_out is not None:
            return grid_out.md5
        return ""

    def get_length(self, filename):
        """ get file size
        """
        grid_out = self.__get_grid_out(filename)
        if grid_out is not None:
            return grid_out.length
        return 0

    def get_content_type(self, filename):
        """
        优先使用fs.files文档中的contentType
        :param filename:
        :return:
        """
        grid_out = self.__get_grid_out(filename)
        if grid_out is not None:
            return grid_out.content_type
        return None

    def __find_or_put(self, filename, content, md5, length, **kwargs):
        """
        在GridFS中查询content是否已经存在，如果存在，返回相应fs.files文档的id；
        如果不存在，就新增引用计数为0的fs.files文档
        :param content: 文件内容
        :param kwargs: 与文件内容有关的元数据，比如content_type、gzipped
        :return: fs.files文档的id
        """
        file_kwargs = dict((k, v) for k, v in kwargs.items() if k in (MetaKey.CONTENT_TYPE, MetaKey.GZIPPED))

        # unique index (md5, length) is needed
        exist_file = self.files.find_one({"md5": md5, "length": length})
        if exist_file is None:
            # 没有找到匹配的文件内容，则存储新的文件内容
            try:
                # the following call returns new-created fs.files document's id
                file_id = self.gfs.put(content, filename=filename, refcount=0, **file_kwargs)
            except (FileExists, DuplicateKeyError) as e:
                logger.warn(traceback.format_exc())
                exist_file = self.files.find_one({"md5": md5, "length": length})
                file_id = exist_file["_id"]
        else:
            file_id = exist_file["_id"]
            logger.debug("found file_id(%s) in fs.files collection" % file_id)

        return file_id

    def save_file(self, filename, content, **kwargs):
        """
            添加一个新的文件到grid_fs
        """
        try:

            assert type(content) == str
            length = len(content)

            assert type(content) == str
            md5 = hashlib.md5(content).hexdigest()

            file_id = self.__find_or_put(filename, content, md5, length, **kwargs)

            return file_id
        except (ResourceClosedError, OperationalError) as e:
            # raised when lock timeout or deadlock found
            logger.warn(traceback.format_exc())

    def get_file(self, object_id):
        """
        获取一个文件，返回一个元组(文件的GridOut对象，文件的metadata)
        """
        try:
            if not type(object_id) == ObjectId:
                object_id = ObjectId(str(object_id))
            grid_out = self.gfs.get(object_id)
            meta_data = {
                'content_type': grid_out.content_type,
                'upload_date': grid_out.upload_date,
                'md5': grid_out.md5,
                'length': grid_out.length
            }

            return grid_out, meta_data
        except NoFile:
            logger.debug(traceback.format_exc())
            logger.warn("No content found for object_id: %s" % object_id)
        return None, None


new_fs = GridFSHelper(setting.REPLICA_SET_URI, setting.REPLICA_SET_DB_NAME, GridFSHelper.REPLICA_SET_CONN)
# new_fs = MixFSHelper("mongodb://192.168.190.129/kr", "kr", MixFSHelper.NORMAL_CONN)

if __name__ == '__main__':
    file_id_test = new_fs.save_file('sunlei', 'Hello SunLei')
    # file_id_test = '533a21053f05e12670a6a2ba'
    grid_out_res, meta_data_res = new_fs.get_file(file_id_test)
    print grid_out_res.read() if grid_out_res else ""
    print meta_data_res