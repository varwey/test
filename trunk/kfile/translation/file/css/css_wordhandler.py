# coding=utf8
'''
Created on Sep 20, 2012

@author: harveyang
'''
from kfile.translation.file.word_handler import WordHandler

class CSSWordHandler(WordHandler):
    
    ext = "css"
    

css_word_handler_instance = CSSWordHandler()