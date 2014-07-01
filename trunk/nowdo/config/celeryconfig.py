# coding=utf8
"""
Created on 2013-08-16
@author: hhl

"""
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange
from nowdo.config import setting


class BaseConfig(object):
    CELERY_ACKS_LATE = True
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_QUEUES = (
        Queue('nowdo_file_extract', Exchange('nowdo_file_extract'), routing_key='nowdo.file.extract'),
        Queue('nowdo_send_mail', Exchange("nowdo_send_mail"), routing_key='nowdo.sendmail'),
    )

    CELERY_ROUTES = {
        "nowdo.tasks.translate.extract_worker": {
            "routing_key": "nowdo.file.extract",
            "queue": "nowdo_file_extract",
        },
        "nowdo.utils.mail.send_mail": {
            "queue": "nowdo_send_mail",
            "routing_key": "nowdo.sendmail",
        },
    }

    CELERY_IMPORTS = (
        'nowdo.tasks.translate',
        'nowdo.utils.mail',
    )

    CELERYBEAT_SCHEDULE = {
    }

    #: Email相关设置
    CELERY_SEND_TASK_ERROR_EMAILS = True
    ADMINS = (
        ('zouyingjun', 'zouyingjun@xingcloud.com'),
        ('sunlei', 'sunlei@xingcloud.com'),
        ('hehuilin', 'hehuilin@xingcloud.com'),
        ('fuluheng', 'fuluheng@xingcloud.com'),
    )
    SERVER_EMAIL = 'DNFS stat info<xcmonitor01@163.com>'
    EMAIL_HOST = 'smtp.163.com'
    EMAIL_HOST_USER = 'xcmonitor01@163.com'
    EMAIL_HOST_PASSWORD = 'xingcloud'
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 10
    BROKER_URL = setting.BROKER_URL

celery = Celery()
celery.config_from_object(BaseConfig)
