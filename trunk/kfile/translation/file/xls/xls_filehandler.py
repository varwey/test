# coding=utf8

from kfile.translation.file.xls.xls_wordhandler import \
    xls_word_handler_instance
from kfile.translation.file.file_handler import FileHandler


class XLSFileHandler(FileHandler):

    word_handler = xls_word_handler_instance
    supported = True
    ext = 'xls'