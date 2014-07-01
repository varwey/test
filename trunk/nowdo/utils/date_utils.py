# coding=utf-8
"""
created by SL on 14-4-23
"""
import datetime

__author__ = 'SL'


def date_delta(value):
    if not isinstance(value, datetime.datetime):
        return 'invalid datetime'
    now = datetime.datetime.now()
    delta_time = now - value
    if delta_time.days > 1:
        if now.year == value.year:
            return value.strftime('%m月%d日')
        return value.strftime('%Y年%m月%d日')

    if delta_time.days == 1 or (delta_time.days == 1 and now.day != value.day):
        return u'昨天'

    seconds = delta_time.seconds
    if seconds < 60:
        return u'刚刚'

    minute = seconds/60
    if minute >= 60:
        return u'%s小时之前' % str(minute/60)

    return u'%s分钟之前' % str(minute)
