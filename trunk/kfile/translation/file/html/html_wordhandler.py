# coding=utf8

from kfile.translation.file.word_handler import WordHandler
from Libs.sgmlparser.sgml.html_util import str2utf8
from Libs.sgmlparser.sgml.html_extract import ExtractHtml
from kfile.utils.kfile_logging import logger

class HTMLWordHandler(WordHandler):
    """
    html 词条handler
    """
    ext = 'html'

    def extract(self, content, user_upload=False):
        """
        抽取
        """
        html_handle = ExtractHtml()
        content = str2utf8(content)[0]
        try:
            word_list, _ = html_handle.get_word_link_list(content)
            tmp_word_list = [word.strip() for word in word_list if word and word.strip()]

        except Exception,e:
            logger.error(e.message)
            tmp_word_list = []

        return list(set(tmp_word_list))

    def integrate(self, content, word_list, user_upload=False):
        """
        合并翻译页面
        """
        word_dict = self._word_list_to_dict(word_list)
        print word_list
        local_html_dict = dict()
        tmp_dict = {}
        for k,v in word_dict.items():
            tmp_dict[k.encode('utf8')] = v.encode('utf8')

        # 补回过滤空格的词条
        html_handle = ExtractHtml()
        content = str2utf8(content)[0]
        full_word_list, link_list = html_handle.get_word_link_list(content)
        for src_word in full_word_list:
            tmp_word = src_word.encode('utf8')
            tmp_word_strip = tmp_word.strip()
            if tmp_word not in tmp_dict and tmp_word_strip in tmp_dict:
                tmp_dict[tmp_word] = tmp_word.replace(tmp_word_strip, tmp_dict[tmp_word_strip])

        local_html_dict['translated_words_dict'] = tmp_dict
        local_html_dict['translated_links_dict'] = {}
        content = html_handle.integrate_html(local_html_dict)
        return content


class HTMWordHandler(HTMLWordHandler):
    """
    htm 词条handler
    """
    ext = 'htm'


html_word_handler_instance = HTMLWordHandler()
htm_word_handler_instance = HTMWordHandler()
