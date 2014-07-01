# -*- coding:utf-8 -*-
import posixpath
from nowdo.config.base import *

__author__ = 'SL'

DEBUG = False

LOG_PATH = '/home/kratos/log/nowdo/'

# 日志设置
LOG_FILE = posixpath.join(LOG_PATH, 'now_do.log')
CELERY_LOG_FILE = posixpath.join(LOG_PATH, 'now_do_celery.log')
FS_LOG_FILE = posixpath.join(LOG_PATH, 'now_do_fs.log')
LOG_LEVEL = 'DEBUG'

MAIN_DB = {
    'host': '10.68.249.172',  # 58.68.249.172
    'db_name': 'nowdo',
    'user': 'kratos_v2',
    'password': '3vUbY52IJ2fJq7KwWPeItNrz8',
}

ACCOUNT_DB = {
    'host': '173.192.182.215',  # 173.192.182.215
    'db_name': 'router',
    'user': 'kratos_v2',
    'password': '3vUbY52IJ2fJq7KwWPeItNrz8',
}

# replica set config
REPLICA_SET_HOST1 = 'idb4.xingcloud.com:27017'
REPLICA_SET_HOST2 = 'idb4.xingcloud.com:37017'
REPLICA_SET_HOST3 = 'idb4.xingcloud.com:47017'
REPLICA_SET_DB_NAME = 'nowdo'
REPLICA_SET_DB_USER = 'kratos'
REPLICA_SET_DB_PWD = 'kratos'
REPLICA_SET_NAME = 'kreplset'
REPLICA_SET_URI = "mongodb://%s:%s@%s,%s,%s/%s?replicaSet=%s" % (
    REPLICA_SET_DB_USER, REPLICA_SET_DB_PWD,
    REPLICA_SET_HOST1, REPLICA_SET_HOST2, REPLICA_SET_HOST3,
    REPLICA_SET_DB_NAME, REPLICA_SET_NAME
)

MEMCACHED_MACHINES = ['10.68.249.172:11211']  # 172

# 机器hostname 到 machine_no 的映射
MACHINE_NO_DICT = {'s0773-sea.hostsud.net': 3, 's0774-sea.hostsud.net': 4, 'cebnqmjh': 5}

BROKER_URL = "amqp://kratos_v2:GZLxVSdOQTIIKGpeoC3vv5Myh@50.23.186.242:5672/NowDo"
