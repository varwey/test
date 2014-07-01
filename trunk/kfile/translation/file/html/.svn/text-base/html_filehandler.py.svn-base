# coding=utf8

from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.html.html_wordhandler import \
    html_word_handler_instance, htm_word_handler_instance


class HTMLFileHandler(FileHandler):
    """
    html文件handler
    """
    word_handler = html_word_handler_instance
    supported = True
    ext = 'html'
    content_type = 'text/html'


class HTMFileHandler(HTMLFileHandler):
    """
    htm文件handler
    """
    word_handler = htm_word_handler_instance
    ext = 'htm'


if __name__ == "__main__":
    import urllib
    doc = urllib.urlopen('http://www.baidu.com')
    word = html_word_handler_instance.extract(doc.read())
    print word,'word'
    word_dict= {}
    for i in word:
        word_dict[i] = 'TTTRRR'

    print  html_word_handler_instance.integrate(doc .read(),word_dict)
