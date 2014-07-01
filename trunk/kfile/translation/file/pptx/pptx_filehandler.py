# -*- coding: utf-8 -*-

# __author__ = "hhl"

from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.pptx.pptx_wordhandler import PptxWordHandler


class PptxFileHandler(FileHandler):
    word_handler = PptxWordHandler()
    supported = True
    ext = 'pptx'
    content_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

