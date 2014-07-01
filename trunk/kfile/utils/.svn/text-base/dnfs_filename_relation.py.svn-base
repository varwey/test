# coding=utf8

#__author__ = 'hhl'

from kfile.setting import REPLICA_SET_URI, REPLICA_SET_DB_NAME
from kfile.utils.kfile_logging import logger
from exceptions import Exception
from pymongo import ReadPreference, ReplicaSetConnection
from bson import ObjectId

def parse_filename(filename):
    """
    将filename解析为四部分：项目名称，语言，无参路径，其他参数
    """
    li = filename.split('?', 1)
    info = li[0].split('/', 2)
    name_info = {}
    if len(info) ==3 and len(info[1]) ==2:
        name_info = {
            "param1": info[0],
            "param2": info[1],
            "param3": info[2]
        }
        if len(li) == 2:
            name_info["param4"]= li[1]
    return name_info


class OperateFilenameRelationException(Exception):
    pass

class NoRelationFound(Exception):
    pass


class FilenameRelation:

    def __init__(self):
        self.uri = REPLICA_SET_URI
        self.dbname =REPLICA_SET_DB_NAME
        self.conn = ReplicaSetConnection(self.uri, read_preference=ReadPreference.PRIMARY)
        self.db = self.conn[self.dbname]
        self.collection = self.db.filename_relation

    def __del__(self):
        if self.db is not None:
            self.conn.close()

    def get(self, filename):
        return self.collection.find_one({"filename":filename})

    def insert(self, filename, object_id, key=None ):
        try:
            has_relation = self.collection.find_one({"filename": filename})
            if has_relation:
                logger.warn("insert failed! There are relation %s in database ", filename)
                return False
            name_info = parse_filename(filename)
            relation = {
                "filename": filename,
                "object_id": object_id,
                "key": key,
                "name_info": name_info
            }

            self.collection.insert(relation)
            return True
        except OperateFilenameRelationException,e:
            logger.error("insert filename_relation error")
            return False

    def rsync(self, filename, **params):
        try:
            relation = self.collection.find_one({"filename": filename})
            name_info = parse_filename(filename)
            if relation:         #若该对应关系存在，则更新记录
                for key, value in params.items():
                    relation[key] = value
                relation["name_info"] = name_info
                self.collection.update({'filename': filename}, relation)
            else:               #该对应关系不存在，则创建新纪录
                if params.has_key("object_id"):
                    new_relation = {"filename": filename}
                    new_relation["name_info"] = name_info
                    for key, value in params.items():
                        new_relation[key] = value
                    self.collection.insert(new_relation)
                else:
                    logger.warn("rsync insert failed! the params of %s error " % filename)
                    return False

            return True
        except Exception,e:
            logger.warn("insert relation_info error")
            print "insert error"
            return False

    def update(self, filename, **params):
        try:
            relation = self.collection.find_one({"filename":filename})
            if relation:
                for key, value in params.items():
                    relation[key] = value
                self.collection.update({'filename': filename}, relation)

                return True

        except OperateFilenameRelationException,e:
            logger.warn("update relation info error")

        return False

    def delete(self, filename, **params):
        try:
            self.collection.remove({'filename': filename})
            return True
        except OperateFilenameRelationException,e:
            logger.warn("delete relation_info error")
            return False

def sync_one_record_to_filename_relation(filename, ** params):
    try:
        filename_relation = FilenameRelation()
        filename_relation.rsync(filename, **params)
    except Exception,e:
        logger.warn("rsync relation_info error")
        return False
    finally:
        if filename_relation.conn:
            filename_relation.conn.close()

def sync_all_fs_relation_to_filename_relation():
    """
    同步文件名称对应关系到mongo中
    """
    from kfile.utils.fs.relation import FSRelation
    from kfile.utils.fs.session import fs_session_cm
    import traceback

    with fs_session_cm() as session:
        try:
            relations = session.query(FSRelation).all()
            if relations is None:
                logger.debug("relation is None, corresponding row must be deleted")
                return

            num =0
            filename_relation = FilenameRelation()
            for relation in relations:
                if filename_relation.rsync(relation.filename, object_id = relation.object_id):
                    num +=1
            logger.debug("Sync %s relation record to filename_relation collection" % num)

        except Exception as e:
            # raised when lock timeout or deadlock found
            logger.warn(traceback.format_exc())

        finally:
            if filename_relation.conn:
                filename_relation.conn.close()

if __name__=="__main__":
    sync_all_fs_relation_to_filename_relation()
    # relation = FilenameRelation()
    # relation.collection.insert({'object_id': ObjectId('518d3112e138230d5900000e'), 'key': "helo"})
    # relation.collection.remove()
    # insert("mltest", 'cn', 'en,fr',1)
    #
    # collection.remove(test_relation)
    # delete({"filename": "mltest"})

