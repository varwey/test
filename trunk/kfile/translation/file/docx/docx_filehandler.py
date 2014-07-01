# -*- coding: utf-8 -*-

from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.word_handler import WordHandler
from kfile.translation.file.docx.docx_wordhandler import DocxWordHandler
from Libs.strs.coding_util import get_unicode

__author__ = "hehuilin"


class DocxFileHandler(FileHandler):
    word_handler = DocxWordHandler()
    supported = True
    ext = 'docx'
    content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

