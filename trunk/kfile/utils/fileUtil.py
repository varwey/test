# coding=utf-8

import os
import codecs
from contextlib import closing
from kfile.utils.kfile_logging import logger


def read_file(path):
    if not os.path.exists(path):
        return ""

    with closing(open(path, 'rb')) as f:
        return f.read()


def write_file(content, path):
    logger.debug("saving %s" %path)

    _dir = os.path.dirname(path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)

    with closing(open(path, 'wb')) as f:
        f.write(content)


def write(tar, pos):
    f = open(pos, 'wb')
    try:
        if type(tar) is str or type(tar) is unicode:
            f.write(tar)
        else:
            f.write(tar.file.read())
    finally:
        f.close()


def save_stream(stream, path):
    
    """
    Store the stream into a file in the FS. 
    """
    
    logger.debug('Saving ' + path)
    try:stream.seek(0) 
    except:pass
    with closing(open(path, 'wb')) as f:
        while True:
            cont = stream.read(1024)
            if len(cont) == 0: break
            f.write(cont)

def escapeForShell(content):
    return content.replace('\'', '\\').encode('utf8')


def remove_bom(content):
    """
    去掉文本文件的BOM头
    只适用于文本文件，不确定是否适用于二进制文件（比如图片、swf、xls）
    refer: http://stackoverflow.com/questions/2456380/utf-8-html-and-css-files-with-bom-and-how-to-remove-the-bom-with-python
    :param content: str类型的文本文件内容
    :return: BOM头, 去掉BOM头后的文件内容
    """
    # 目前只支持content为str类型
    if type(content) != str:
        return None, content

    bom_info = (
        (codecs.BOM_UTF32_LE, 4),   # BOM头长些的排在前面
        (codecs.BOM_UTF32_BE, 4),
        (codecs.BOM_UTF8, 3),
        (codecs.BOM_UTF16_LE, 2),
        (codecs.BOM_UTF16_BE, 2),
    )

    for bom, length in bom_info:
        if content.startswith(bom):
            return bom, content[length:]

    return None, content


if __name__ == '__main__':
    s1 = "\xef\xbb\xbfHello, world!"
    s2 = "Hello, world!"
    s3 = "hi"
    s4 = "\xef\xbbHello, world!"
    s5 = "\xff\xfe\x00\x00Hello, world!"
    s6 = "\xff\xfeHello, world!"
    print remove_bom(s1)
    assert remove_bom(s1)[1] == s2
    print remove_bom(s2)
    assert remove_bom(s2)[1] == s2
    print remove_bom(s3)
    assert remove_bom(s3)[1] == s3
    print remove_bom(s4)
    assert remove_bom(s4)[1] == s4
    print remove_bom(s5)
    assert remove_bom(s5)[1] == s2
    print remove_bom(s6)
    assert remove_bom(s6)[1] == s2
    pass