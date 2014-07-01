# coding=utf-8

from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.json.json_wordhandler import json_word_handler_instance


class JSONFileHandler(FileHandler):

    word_handler = json_word_handler_instance
    supported = True
    ext = 'json'
    content_type = 'application/json'


if __name__ == "__main__":
    with open("F:\\word_task_get.json", "rb") as f:
        content = f.read()
        json_handler = JSONFileHandler()

        word_list = json_handler.word_handler.extract(content)

        word_dict = dict()
        for word in word_list:
            print word
            word_dict[word] = word + "translated"

        content = json_handler.word_handler.integrate(content, word_dict)
        print type(content)
        if isinstance(content, unicode):
            print content.encode('utf8')
        else:
            print content