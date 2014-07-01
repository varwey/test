# coding=utf-8

import json
from kfile.translation.file.word_handler import WordHandler
from Libs.strs.coding_util import get_unicode
from kfile.utils.kfile_logging import logger

class JsonLoadsException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def json_word_parser(data, p, key, ret, word_dict=None):
    """
        递归提取和合成json格式文件
    """
    data_type = type(data)
    if data_type in (str, unicode) and data.strip():
        if word_dict is not None and data in word_dict:     # integrate
            p[key] = word_dict[data]
        else:                       # extract
            ret.append(data)
    elif data_type == dict:
        for elem in data:
            json_word_parser(data[elem], data, elem, ret, word_dict)
    elif data_type == list:
        for elem in data:
            json_word_parser(elem, data, data.index(elem), ret, word_dict)


class JSONWordHandler(WordHandler):

    ext = 'json'

    def extract(self, content, user_upload=False):
#        content = content.decode("utf-8-sig")
        content = get_unicode(content)
        try:
            data = json.loads(content)
        except Exception,e:
            try:
                if u"\ufeff" == content[:1]:
                    data = json.loads(content[1:])
                else:
                    raise JsonLoadsException(e)
            except Exception,e:
                raise JsonLoadsException(e)

        words = []
        json_word_parser(data, None, None, words)
        return words

    def integrate(self, content, word_list, user_upload=False):
#        content = content.decode("utf-8-sig")
        word_dict = self._word_list_to_dict(word_list)
        content = get_unicode(content)
        try:
            data = json.loads(content)
        except Exception,e:
            try:
                if u"\ufeff" == content[:1]:
                    data = json.loads(content[1:])
                else:
                    raise JsonLoadsException(e)
            except Exception,e:
                raise JsonLoadsException(e)

        json_word_parser(data, None, None, None, word_dict)
        return json.dumps(data, ensure_ascii=False).encode("utf8")


json_word_handler_instance = JSONWordHandler()


if __name__ == "__main__":
#     word = u'''{
#     "family":"kratos",
#     "name":"translate",
#     "version":"0.0.1",
#     "spm": {
#         "source": "src",
#         "output":["translate.js"],
#         "alias": {
#             "$": "$",
#             "underscore": "gallery/underscore/1.4.2/underscore",
#             "backbone": "gallery/backbone/0.9.9/backbone",
#             "json": "gallery/json/1.0.2/json",
#             "utils":"kratos/utils/2.1.1/utils",
#             "libs": "kratos/libs/1.0.6/libs"
#         }
#     }
# }'''
#     sub_words = json_word_handler_instance.extract(word)
#     print "***********************************"
#     import pprint
#     pprint.pprint(sub_words)

    # sub_word_dict = dict()
    # for sw in sub_words:
    #     print sw
    #     sub_word_dict[sw] = sw + "translated"
    #
    # print json_word_handler_instance.integrate(word, sub_word_dict)
    # from kfile.translation.file.xml.xml_wordhandler import xml_word_handler_instance
    filename = "/root/share/test.xml"
    # fread = open(filename, 'r')
    # xml_content = fread.read()
    # fread.close()
    #
    # word_list = xml_word_handler_instance.extract(xml_content, user_upload=True)
    from kfile.translation.file.xml.xpath import StandardException
    # print '\nword_list:'
    # for word in word_list:
    #     print word