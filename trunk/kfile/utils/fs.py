#!-*- coding:utf8 -*-
from kfile.utils.kfile_logging import logger
from kfile import setting
import ujson
import requests
import traceback

def send_request(url, method='GET', **kwargs):
    """请求 DNFS API"""
    try:
        if method=='POST':
            print url, kwargs
            rep = requests.post(url, kwargs)
        else:
            rep = requests.get(url)
        return ujson.loads(rep.text)['result']
    except Exception as e:
        logger.error('request dnfs api. url:%s, error:%s' % (url, traceback.format_exc()))


def delete(filename):
    if type(filename) != 'list':
        filename = [filename]
    url = '%s/%s' % (setting.DNFS_API, 'delete')
    params = {
        'filename': filename,
    }
    return send_request(url, method='POST', **params)