#coding=utf8
__author__ = 'T510'

import re
xc_version_tig = "xcv="
xc_re_obj = re.compile(xc_version_tig+'[0-9]*')


def _add_xcv(url, xcv):
    standard_url = url
    if xcv:
        if '?' in url:
            standard_url += '&%s%s'%(xc_version_tig, xcv)
        else:
            standard_url += '?%s%s'%(xc_version_tig, xcv)

    return standard_url