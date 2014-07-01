# -*- coding: utf-8 -*-
"""
定制的Base
"""
import os
import time
import datetime
import threading
import sqlalchemy as SA
from sqlalchemy.orm import object_session
from sqlalchemy.ext.declarative import declarative_base
from nowdo.config import setting


class tBase(object):
    session = property(lambda self: object_session(self))

    created_date = SA.Column(SA.DateTime, default=datetime.datetime.now)
    modified_date = SA.Column(SA.DateTime, default=datetime.datetime.now, onupdate=SA.text('current_timestamp'))


machine_no = None


def get_machine_no():
    """
    从环境变量获取机器编号
    """
    #    machine_no_str = os.environ.get('MACHINE_NO')
    global machine_no
    if not machine_no:
        import socket

        host = socket.gethostname()
        machine_no = setting.MACHINE_NO_DICT.get(host, None)
        if machine_no is None:
            raise Exception("HOSTNAME: %s is not in the MACHINE_NO_DICT. Please check configuration. " % host)

    return machine_no

# 目前支持的机器编号范围为0~15，每个机器一个机器编号，不允许重复
MACHINE_NO = get_machine_no()


class IdGenerator(object):
    _inc = 0
    _inc_lock = threading.Lock()

    _machine_no = MACHINE_NO

    @staticmethod
    def generate():
        # 32 bits time
        id = (int(time.time()) & 0xffffffff) << 32
        # 4 bits machine number
        id |= (IdGenerator._machine_no & 0xf) << 28
        # 8 bits pid
        id |= (os.getpid() % 0xFF) << 20
        # 20 bits increment number
        IdGenerator._inc_lock.acquire()
        id |= IdGenerator._inc
        IdGenerator._inc = (IdGenerator._inc + 1) % 0xFFFFF
        IdGenerator._inc_lock.release()

        return id


def id_generate():
    return IdGenerator.generate()


Base = declarative_base(cls=tBase)

#: 是否在标准输出流打印sql语句(sqlalchemy)
echo = setting.ECHO_SQL

main_db_info = setting.MAIN_DB

main_db_engine = SA.create_engine(
    'mysql://%s:%s@%s/%s?charset=utf8' % (main_db_info['user'], main_db_info['password'],
                                          main_db_info['host'], main_db_info['db_name']),
    echo=echo,
    pool_recycle=3600,
    pool_size=15
)

metadata = Base.metadata