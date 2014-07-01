# coding=utf8
'''
Created on Aug 20, 2012

@author: harveyang
'''

from Libs.sgmlparser.base_i18n_worker import BaseI18NWorker
import re
from Libs.sgmlparser.constant import ATTR_WORD_LIST, DEFAULT_BUM_TRANS_RULE, DEFAULT_INVALID_WORD_RULE


class TextI18NWorker(BaseI18NWorker):
    #------ HTML textNode 处理-----#
    worker_flag = 'text'

    def extract(self, line_element, attr_list=ATTR_WORD_LIST):
        """
        提取html页面内的textnode 和 自定义属性值ATTR_WORD_LIST 对应的翻译元素
        :param line_element:
        :param attr_list:
        :return:  抽取出的word list
        """
        word_list = []
        tmp_data = line_element.data.strip()
        if 'text' == line_element.e_type and tmp_data is not '' and not re.match(DEFAULT_BUM_TRANS_RULE, tmp_data):
            # 判断取出的textnode是不是经过js和css替换处理的临时替换，如果是则不提取
            if not tmp_data.startswith("XCXCXCXCXCXCXCXCX"):
                word_list.append(line_element.data)
        return word_list

    pass

    def integrate(self, line_element, words_dict, attr_list=ATTR_WORD_LIST):
        """
        译文替换, 在替换的过程中,进行判断是否需要进行替换.在此应用一些规则
        :param line_element: 片段元素
        :param words_dict:   翻译好的字典对
        :param attr_list:
        :return:
        """
        if 'text' == line_element.e_type:
            # 货币+价格 忽略翻译
            if re.match(DEFAULT_BUM_TRANS_RULE, line_element.data.strip()):
                # 进行xc_no_trans 属性进行判断, 是否需要翻译
                return line_element
            # 垃圾字符 忽略翻译
            tmp = DEFAULT_INVALID_WORD_RULE.sub('', line_element.data.strip())
            if not tmp.strip(''):
                return line_element
            # 翻译处理
            if words_dict.has_key(line_element.data):
                line_element.update_word(words_dict[line_element.data])
        return line_element

    pass
