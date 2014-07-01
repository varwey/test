# -*- coding:utf-8 -*-
import posixpath
from nowdo.config.base import *
__author__ = 'SL'

ECHO_SQL = False

DEBUG = True

# 日志设置
LOG_FILE = posixpath.join(LOG_PATH, 'now_do.log')
CELERY_LOG_FILE = posixpath.join(LOG_PATH, 'now_do_celery.log')
FS_LOG_FILE = posixpath.join(LOG_PATH, 'now_do_fs.log')
LOG_LEVEL = 'DEBUG'

MAIN_DB = {
    'host': '10.1.15.195',
    'db_name': 'nowdo',
    'user': 'kratos_v2',
    'password': 'd9U6ooizh7v6SrCYdr8iC5Wwh',
}  # CREATE SCHEMA `cooperation` DEFAULT CHARACTER SET utf8 ;

MEMCACHED_MACHINES = ['10.1.15.194:11211']

REPLICA_SET_HOST1 = '10.1.15.191:27017'
REPLICA_SET_HOST2 = '10.1.15.191:37017'
REPLICA_SET_HOST3 = '10.1.15.191:47017'
REPLICA_SET_DB_NAME = 'nowdo'
REPLICA_SET_DB_USER = 'kratos'
REPLICA_SET_DB_PWD = 'kratos'
REPLICA_SET_NAME = 'repltest'
REPLICA_SET_URI = "mongodb://%s:%s@%s,%s/%s?replicaSet=%s" % (REPLICA_SET_DB_USER, REPLICA_SET_DB_PWD,
                                                              REPLICA_SET_HOST1, REPLICA_SET_HOST2,
                                                              REPLICA_SET_DB_NAME, REPLICA_SET_NAME)

#: 机器hostname 到 machine_no 的映射。机器编号范围为0~15
MACHINE_NO_DICT = {
    'mldev197': 1,
    'LIUXIONG-PC': 2,
    'zou-VirtualBox': 15,
    'onfirenbpc': 14,
    'localhost.localdomain': 13,
    'JPZQSGCI91TT5SE': 11,
    'pro-MacB.local': 3,
    'zhoumatoMacBook-Pro.local': 5,
    'localhost': 9,
    'ubuntu': 33,
    'Admin-PC': 10,
    'xujiawan': 4,
    'T510-THINK': 6,
    'zou-THINK': 12,
    'ruiqi-laptop': 99,
    'zhaojl-PC': 88,
    'ml-test': 7,
    'test191': 8,
    'ZouYingjunMBP.local': 7,
    'Zou-PC': 15,
    'jamonhe-VirtualBox': 15,
    'Sarike-PC': 2,
    'bogon': 13,
    'johnny-MS-7680': 15,
    'wangweiwei-machine': 14
}


CAS_ENABLE = False
CAS_SERVER_URL = "http://10.1.15.194:8080/cas"

BROKER_URL = "amqp://kratos:GZLxVSdOQTIIKGpeoC3vv5Myh@10.1.15.194:5672//"

