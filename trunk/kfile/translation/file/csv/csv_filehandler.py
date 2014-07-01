# coding=utf-8
__author__ = 'yanggaoxiang'

from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.csv.csv_wordhandler import csv_word_handler_instance

class CSVFileHandler(FileHandler):

    word_handler = csv_word_handler_instance
    supported = True
    ext = 'csv'

if __name__ == "__main__":
    file = open('lang.csv', 'r')
    content = file.read()
    print content
    handler = CSVFileHandler()
    words = handler.word_handler.extract(content)
    print words
    word_dict = {}
    for word in words[1:]:
        word_dict[word] = "hahaha" + word
    content = handler.word_handler.integrate(content, word_dict)
    print content