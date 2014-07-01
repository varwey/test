'''
Created on 2012-2-6

@author: admin
'''
from urlparse import urlparse
from kfile import setting


class RequestAddressError(Exception):
    pass


def behead(url):
    url_info = urlparse(url)
    head_index = len(url_info.scheme) + len(url_info.netloc) + 4
    return url[head_index:]


def parse_req_addr(url):
    # tail should be like "group_name/lang/source"
    tail = behead(url)
    ret = {}
    elements = tail.split('/', 2)
    if len(elements) != 3:
        raise RequestAddressError('wrong request address')

    for elem in elements:
        if not elem:
            raise RequestAddressError('wrong request address')

    ret['group_name'] = elements[0]
    ret['lang'] = elements[1]
    ret['source'] = elements[2]

    return ret


def parse_resource_addr(url):
    o = urlparse(url)
    host = ''
    if o.netloc:
        host = o.scheme + '://' + o.netloc
    path = o.path.lstrip('/')
    return dict(host=host, path=path)

import re
param_pat = re.compile(r'(&?xc_md5=[a-zA-Z0-9]*)|(&?_xingcloud_t=[a-zA-Z0-9]*)|(&?xcv=[a-zA-Z0-9]*)')

def remove_xc_params(addr):
    return re.sub(param_pat, lambda g: "", addr).strip('?')



if __name__ == '__main__':
    url = 'http://localhost/ysm/cn/t.xingclsd.xmo/swf/sfd/dd.xml'
    print parse_req_addr(url)

    print parse_resource_addr(url)

    print parse_resource_addr('http://www.baidu.com')

    print parse_req_addr('http://10.1.4.200/haidao/pt/xc.lp.fminutes.us/program/files/ONEFIGHT__b4932881.swf?1332299685718')

    print remove_xc_params('http://localhost/ysm/cn/t.xingclsd.xmo/swf/sfd/dd.xml?t=5455&p=3&md5=023423xcvsa')
    print remove_xc_params('http://localhost/ysm/cn/t.xingclsd.xmo/swf/sfd/dd.xml?md5=023423xcvsa')
    print remove_xc_params('http://localhost/ysm/cn/t.xingclsd.xmo/swf/sfd/dd.xml?t=5455&p=3&md5=023423xcvsa&md5=023423xcvsa&md5=023423xcvsa')
    print remove_xc_params('http://localhost/ysm/cn/t.xingclsd.xmo/swf/sfd/dd.xml?t=5455&p=3&md5=&_xingcloud_t=023423xcvsa')

    print parse_resource_addr('http://wiki.open.qq.com/wiki/%E5%B9%B3%E5%8F%B0%E5%8A%A8%E6%80%81#API.E6.9B.B4.E6.96.B0')