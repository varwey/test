# -*- coding=utf-8 -*-
import copy
import mimetypes
import os
__author__ = 'zou'

__all__ = ['mime_types', 'image_mime_types', 'video_mime_types', 'readable_mime_types', 'guess_type']

__mime_types_file_path__ = os.path.join(os.path.dirname(__file__), 'mime.types')
mimetypes.init([__mime_types_file_path__])

__readable_to_mode_map__ = {
    u'text/html': u'html',
    u'application/javascript': u'javascript',
    u'text/javascript': u'javascript',
    u'application/x-javascript': u'javascript',
    u'text/css': u'css',
    u'application/json': u'json',
    u'text/json': u'json',
    u'x-json': u'json',
    u'application/xml': u'xml',
    u'text/xml': u'xml',
    }

FLASH_MIME_TYPE = 'application/x-shockwave-flash'

def __readable_suffix():
    return [
        u'.json',
        u'.js',
        u'.css',
        u'.po',
        u'.properties',
        u'.htm',
        u'.html',
        u'.xml',
        u'.csv'
    ]

def __image_mime_type_ex():
    return [
        u'image/jpg',
        u'image/x-icon',
        u'image/pjpeg',
        ]

def __readable_mime_type_ex():
    return [
        u'application/javascript',
        u'application/x-javascript',
        u'X-JSON',
        u'application/xml',
        u'text/json'
    ]


def get_mode(type):
    if type:
        return __readable_to_mode_map__.get(type, 'text')
    return 'text'

def guess_type(filename, strict=True):
    return mimetypes.guess_type(filename, strict)

def image_mime_types():
    return __get_mime_with_types('image') + __image_mime_type_ex()

def video_mime_types():
    return __get_mime_with_types('video')

def readable_mime_types():
    ret = __readable_mime_type_ex()
    for k, v in mimetypes.types_map.items():
        if v.startswith('text/') or k in __readable_suffix():
            if v not in ret:
                ret.append(v)
    return ret

def __get_mime_with_types(type):
    ret = []
    for key, val in mimetypes.types_map.items():
        if val.startswith(type):
            ret.append(val)

    return ret

if __name__ == "__main__":
    print image_mime_types()
    print video_mime_types()
    print readable_mime_types()