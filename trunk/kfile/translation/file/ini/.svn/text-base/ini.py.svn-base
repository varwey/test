# -*- coding: utf-8 -*-
import re
from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.ini.word_extractor import WordExtractor
from Libs.strs.coding_util import get_unicode
from kfile.translation.file.word_handler import WordHandler
__author__ = 'yeshiming@gmail.com'

class INIWordGen(object):

    OPTCRE_NV = re.compile(
        ur'^\s*(?P<option>[^:=\s;\[][^:=]*)'          # very permissive!
        ur'\s*(?:'                             # any number of space/tab,
        ur'(?P<vi>[:=])\s*'                    # optionally followed by
        # separator (either : or
        # =), followed by any #
        # space/tab
        ur'(?P<value>.*?))\r?$'                   # everything up to eol
        ,
        re.MULTILINE|re.UNICODE
    )

    def __init__(self, content):
        self.content = content

    def pop(self):
    #        print re.findall(self.OPTCRE_NV, self.content)
        for m in re.finditer(self.OPTCRE_NV, self.content):
            yield m.start('value'), m.end('value'), get_unicode(m.group('value'))


def extract(content):
    we = WordExtractor(content, INIWordGen)
    return we.extract_words()

def integrate(content, entry_list):
    we = WordExtractor(content, INIWordGen)
    return we.insert_words(entry_list)

class INIWordHandler(WordHandler):

    ext = 'ini'

    def extract(self, content, user_upload=False):
        """
        抽取
        """
        return [get_unicode(i) for i in extract(get_unicode(content))]

    def integrate(self, content, word_list, user_upload=False):
        # word_dict = self._word_list_to_dict(word_list)
        return integrate(get_unicode(content), word_list).encode('utf8')

        # return integrate(get_unicode(content), dict(
        #     (k, v)
        #         for k, v in word_dict.iteritems()
        #     )
        # ).encode('utf8')


handler = INIWordHandler()

class INIFileHandler(FileHandler):

    word_handler = handler
    supported = True
    ext = 'ini'
    content_type = "text/ini"


if __name__ == '__main__':
    rb__read = open("edesk.ini", 'rb').read()
    a =  extract(rb__read)
#    for i in a:
#        print i
    print integrate(rb__read, dict(
        (get_unicode(i), get_unicode(i) + u'translated') for i in a
    ))

