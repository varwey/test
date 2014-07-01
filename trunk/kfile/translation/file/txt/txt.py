# -*- coding: utf-8 -*-
import re
from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.word_handler import WordHandler
from Libs.strs.coding_util import get_unicode, str2utf8

__author__ = 'yeshiming@gmail.com'

class TXTWords(WordHandler):
    ext = 'txt'

    def extract(self, content, user_upload=False):
        return [entry for entry in get_unicode(content).splitlines()]

    def integrate(self, content, word_list, user_upload=False):
        """
        :param word_list: a list store relation of src_words and their translate result, such as [(src1, trans1),(src2, trans2)]
        """
        # word_dict = self._word_list_to_dict(word_list)
        words_dict = {}
        for entry in word_list:
            words_dict[entry[0]] = entry[1]

        content = get_unicode(content)
        content_list = [con for con in content.splitlines()]
        new_content_list = []

        i = 0
        for con in content_list:
            tar_word, i = self.replace_or_origin(con, i, word_list, words_dict)

            new_content_list.append(str2utf8(tar_word)[0])

        return '\r\n'.join(new_content_list)
        # return '\r\n'.join(word_dict.get(line, line) for line in content.splitlines()).encode('utf8')

class TXTFileHandler(FileHandler):

    word_handler = TXTWords()
    supported = True
    ext = 'txt'
    content_type = "text/plain"


if __name__ == '__main__':
    import pprint
    from kfile.controls.session import sessionCM
    from kfile.controls.file import File
    group_name = "last"
    file_id = "5940197244288368659"
    with sessionCM(group_name=group_name) as session:
        file = session.query(File).get(file_id)
        entry_list = [entry.entry.word for entry in file.entries_pos]

        i = 0
        print "****************************************", len(entry_list)
        # pprint.pprint(entry_list)
        for entry in entry_list:
            if i < 20:
                print entry
            i += 1