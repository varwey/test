# -*- coding: utf-8 -*-

from contextlib import closing


CODE_LIST_TO_TRY = ('utf8', 'shift-jis', 'euc-jp', 'gbk', 'ISO-8859-2', 'gb2312', 'utf16', 'utf32', 'big5',)


def str2utf8(str):
    if isinstance(str, unicode):
        try:
            return str.encode('utf8'), "utf8"
        except:
            pass

    for c in CODE_LIST_TO_TRY:
        try:
            return str.decode(c).encode('utf8'), c
        except:
            pass

    return str, ""


def get_unicode(str):
    if isinstance(str, unicode):
        return str

    for c in CODE_LIST_TO_TRY:
        try:
            return str.decode(c)
        except:
            pass

    return str


def convert_file_to_utf8(path):
    with closing(open(path, "r")) as f:
        content = f.read()
    content = get_unicode(content)
    with closing(open(path, 'w')) as f:
        f.write(content)
