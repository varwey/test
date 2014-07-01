# coding=utf-8
"""
created by SL on 14-3-7
"""
from nowdo.config.celeryconfig import celery

__author__ = 'SL'


def send_mail(subject, message, receivers, cc=None, bcc=None):
    if type(receivers) != list:
        receivers = [receivers, ]
    celery.send_task("nowdo.utils.mail.send_mail", [subject, message, receivers, cc or [], bcc or []])


if __name__ == '__main__':
    send_mail("Subject", "Message", 'sarike@timefly.cn')