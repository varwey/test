# coding=utf-8
from kfile.translation.file.ini.ini import INIWordHandler

__author__ = 'yanggaoxiang'

from kfile.translation.file.file_handler import FileHandler

ini_word_handler = INIWordHandler()
ini_word_handler.ext='properties'

class PROPERTIESFileHandler(FileHandler):

    word_handler = ini_word_handler
    supported = True
    ext = 'properties'
    content_type = "text/properties"



if __name__ == "__main__":
    file = open('test2.properties', 'r')
    content = file.read()
    print content
    handler = PROPERTIESFileHandler()
    words = handler.word_handler.extract(content)
    print words
    word_dict = {}
    for word in words[1:]:
        word_dict[word] = "hahaha" + word
    content = handler.word_handler.integrate(content, word_dict)
    print content
