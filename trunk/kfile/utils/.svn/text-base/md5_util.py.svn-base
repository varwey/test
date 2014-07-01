# coding=utf-8

import hashlib
from kfile.utils.coding_util import str2utf8


def get_md5(str):
    """
    str: 字符串
    return: 16 bytes digest
    """
    m = hashlib.md5()
    m.update(str2utf8(str)[0])
    return m.digest()


def get_hex_md5(str):
    m = hashlib.md5()
    m.update(str2utf8(str)[0])
    return m.hexdigest()


def binary2md5(binary_content):
    m = hashlib.md5()
    m.update(binary_content)
    return m.hexdigest()


if __name__ == '__main__':
    print get_md5("你好！World!")
    print get_hex_md5("你好！World!")
    print binary2md5(get_md5("你好！World!"))