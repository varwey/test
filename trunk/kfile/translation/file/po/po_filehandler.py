# coding=utf-8
__author__ = 'yanggaoxiang'

from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.po.po_wordhandler import po_word_handler_instance

class POFileHandler(FileHandler):

    word_handler = po_word_handler_instance
    supported = True
    ext = 'po'
    content_type = "text/po"


if __name__ == "__main__":
    file = open('lang.po', 'r')
    content = file.read()
    print content
    handler = POFileHandler()
    words = handler.word_handler.extract(content)
    print words
    word_dict = {}
    for word in words[1:]:
        word_dict[word] = "hahaha" + word
    content = handler.word_handler.integrate(content, word_dict)
    print content