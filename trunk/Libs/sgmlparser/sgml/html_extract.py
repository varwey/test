#-*- coding=utf-8 -*-
from Libs.strs.coding_util import get_unicode
from html_parse_utils import gen2list, LineElement
from Libs.sgmlparser.sgml.html_util import html_jsscript_extract, html_css_extract, modify_meta_charset2utf8, html_replace_integrate
from Libs.sgmlparser.attr_i18n_worker import AttrI18NWorker
from Libs.sgmlparser.text_i18n_worker import TextI18NWorker
from Libs.sgmlparser.url_i18n_worker import UrlI18NWorker
from sgml_xc_parser import SGMLParser


class ExtractStructure(object):
    """
    解析html内容，返回可翻译内容
    """

    def __init__(self, content):
        """
        初始化解析器
        """
        self.content = content
        self.parser = SGMLParser()
        pass

    def pop_element(self):
        # 返回的是(e_type, (i,j), data)
        self.html_structure = self.parser.parser_structure(self.content)
        for item in self.html_structure:
            if isinstance(item, tuple):
                p = LineElement(item)
                if p.data is not None: yield p
        pass


class ExtractHtml(object):
    """
    html 抽取 合并（包含翻译）

    """

    def __init__(self):
        self.i18n_worker_list = [TextI18NWorker, UrlI18NWorker, AttrI18NWorker]
        self.i18n_worker_list_instance = [handler() for handler in self.i18n_worker_list]
        self.element_list = []
        self.content = ''
        self.script_dict = {}
        self.css_dict = {}

    def pre_html2list(self, content):
        """
        预处理
        """
        #对html中的javascript和style中编写的css做预处理，提取出标签内容
        self.content, self.script_dict = html_jsscript_extract(content)
        self.content, self.css_dict = html_css_extract(self.content)

        #----------解析html为对象序列----------#
        gen = ExtractStructure(self.content).pop_element()
        self.element_list = gen2list(gen)
        return self.element_list


    def get_segments(self, content):
        element_list = self.pre_html2list(content)
        return [line_element.data for line_element in element_list]


    def get_word_link_list(self, content):
        """
        抽取所给html内容的词条和连接
        对于wordlist应该除掉XCXCXCXCXCXCXCXCX
        """
        # 对html中的javascript和style中编写的css做预处理，提取出标签内容
        self.element_list = self.pre_html2list(content)

        link_list, word_list = [], []
        for line_element in self.element_list:
            if line_element.e_type not in ['text', 'start_tag']:
                continue
            for handler in self.i18n_worker_list_instance:
                tmp_value_list = handler.extract(line_element)
                for i in tmp_value_list:
                    i_strip = i.strip()
                    if handler.worker_flag in ['text', 'attr'] and i_strip:
                        word_list.append(i)
                    if 'url' == handler.worker_flag and i_strip:
                        link_list.append(i)
        word_list, link_list = list(set(word_list)), list(set(link_list))

        #----  过滤 js和css替换的词条----#
        tmp_word_list = [get_unicode(item) for item in word_list if "XCXCXCXCXCXCXCXCX" not in item]

        return tmp_word_list, link_list
        pass

    def integrate_html(self, local_aux_file_dict):
        """
        合并
        :param local_aux_file_dict:
        :return: 翻译好的页面内容
        """
        for i in xrange(len(self.element_list)):
            element = self.element_list[i]
            for handler in self.i18n_worker_list_instance:
                if handler.worker_flag in ["text", "attr"]:
                    translated_dict = local_aux_file_dict['translated_words_dict']
                elif 'url' == handler.worker_flag:
                    translated_dict = local_aux_file_dict['translated_links_dict']
                else:
                    translated_dict = {}
                    # 此处同一个element可以被handle两次（词条替换和连接替换）
                element = handler.integrate(element, translated_dict)

        self.content = ''.join([element_html.data for element_html in self.element_list\
                                if element_html])
        #-------html 尾处理-------#
        self.content = modify_meta_charset2utf8(self.content)
        self.content = html_replace_integrate(self.content, self.script_dict)
        self.content = html_replace_integrate(self.content, self.css_dict)
        return self.content


def test_html_extract_and_integrate():
    import urllib

    p = ExtractHtml()
    dc = urllib.urlopen(
        "http://www.dresses123.com/astonishing-aline-chiffon-one-shoulder-shortmini-homecoming-dresses-p-615.html")
    from Libs.sgmlparser.sgml.html_util import str2utf8

    word_list, link_list = p.get_word_link_list(str2utf8(dc.read())[0])
    local_aux_file_dict = dict()
    tmp_dict = dict()
    for i in word_list:
        i = str2utf8(i)[0]
        tmp_dict[i] = i + "Trans"
    local_aux_file_dict['translated_words_dict'] = tmp_dict
    local_aux_file_dict['translated_links_dict'] = {}
    print p.integrate_html(local_aux_file_dict)

if __name__ == '__main__':
    test_html_extract_and_integrate()

#    import cProfile
#    cp = cProfile.Profile()
#    cp.run("test_html_extract_and_integrate()")
#    cp.print_stats()
