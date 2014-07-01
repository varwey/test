# coding=utf8

"""
user-defined mysql types
"""

import json
import sqlalchemy.types
from bson import ObjectId


# 自定义类型
class MySQLObjectId(sqlalchemy.types.TypeDecorator):
    """MongoDB中的ObjectID的包装
    """

    impl = sqlalchemy.types.BINARY

    def process_bind_param(self, value, dialect):
        """convert ObjectId object to its binary representation
        """
        if value is not None:
            try:
                # validate value.
                # if value is not None, ObjectId's __init__ method will call __validate
                return ObjectId(oid=value).binary
            except:
                pass

        return None


    def process_result_value(self, value, dialect):
        """convert binary representation to ObjectId object
        """
        if value is not None:
            try:
                return ObjectId(value)
            except:
                pass

        return None


class MySQLDict(sqlalchemy.types.TypeDecorator):
    """Python dict的包装
    """

    impl = sqlalchemy.types.Text

    def process_bind_param(self, value, dialect):
        """convert dict object to json string
        """
        if isinstance(value, dict):
            return json.dumps(value)
        return json.dumps({})


    def process_result_value(self, value, dialect):
        """convert json string to dict object
        """
        return json.loads(value)