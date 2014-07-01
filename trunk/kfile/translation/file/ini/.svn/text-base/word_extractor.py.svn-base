# -*- coding: utf-8 -*-

from Libs.strs.coding_util import get_unicode
from Libs.sgmlparser.sgml.sgml_xc_parser import SGMLParser
from kfile.utils.translate.file_integrate import replace_or_origin

class Parser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)

class WordGenerator(object):
    def __init__(self, content):
        self.content = content
        self.parser = Parser()
        self.html_structure = self.parser.parser_structure(self.content)

    def pop(self):
        """
        生成器
        """
        #        #####stub
        #        i = next = 0
        #        word = 'word'
        #        while True:
        #            i = self.content.find(word, next)
        #            #            print 'found', i
        #            next = i + len(word)
        #            if i == -1:
        #                break
        #            yield i, next, word
        #            #####stub
        for item in self._get_text():
            yield item[1][0], item[1][1], item[2]
        pass


    def _get_text(self):
        for item in self.html_structure:
            if 'text' == item[0] :
                yield item
            else:
                continue
        pass

    def _handle_text_node(self, start, end):
        pass

    def _handle_attribute(self, start, end, tag, key, value):
        pass


class WordExtractor(object):
    def __init__(self, content, generator=None):
        self.content = content
        if not generator:
            generator = WordGenerator
        self.word_gen = generator(content)
        self.word_list = [t for t in self.word_gen.pop()]

    def extract_words(self):
#        self.word_list = [t for t in self.word_gen.pop()]
        return [word for a, b, word in self.word_list]

    def insert_words(self, entry_list):
        print 'word_list',self.word_list
        words_dict = {}
        for entry in entry_list:
            words_dict[entry[0]] = entry[1]

        new_word_list = []
        i = 0
        for s, e, word in self.word_list:
            tar_word, i = replace_or_origin(word, i, entry_list, words_dict)
            new_word_list.append((s, e, tar_word))

        # new_word_list = [(s, e, word_dict.get(word, word)) for s, e, word in self.word_list]
        segments = [get_unicode(word) for word in self.__get_segment(new_word_list)]
        return "".join(segments)

    def __get_segment(self, word_list):
        i = 0
        for start, end, word in word_list:
            if i != start:
#                print 'seg', self.content[i: start]
                yield self.content[i: start] # 间隔
#            print 'seg', word
            yield word
            i = end
        if i != len(self.content):
#            print 'seg', self.content[i:]
            yield self.content[i:]

    def get_segments(self):
        return [segment for segment in self.__get_segment(self.word_list)]


def test_word_extractor():
    content = """
word
word
word
word
word
wefd
word
word
word
word
"""
    we = WordExtractor(content)
    words = we.extract_words()
    print words
    assert words == ['word', 'word', 'word', 'word', 'word', 'word', 'word', 'word', 'word']
    word_dict = dict([('word', 'good-word')])
    result = we.insert_words(word_dict)
    print 'orig:', content
    print 'result:', result
    assert result == """
good-word
good-word
good-word
good-word
good-word
wefd
good-word
good-word
good-word
good-word
"""

if __name__ == "__main__":
#    test_word_extractor()
    CONTENT = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>BIKE</title>
<script src="http://www.google.com/jsapi" title='nice'></script>
</head>
<body>
<img><h1>good<span>NEWS</span>good</h1>
<a>&nbsp;H&nbsp;H&nbsp;H&nbsp;</a>
</body>
</html>'''
    we = WordExtractor(CONTENT)
    words = we.extract_words()
    print words