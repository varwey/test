#-*- coding=utf-8 -*-
import re
from Libs.sgmlparser.base_i18n_worker import BaseI18NWorker
from constant import ATTR_WORD_LIST, NOT_TRANS_TAG, ATTR_ON, IGNORE_TAG, DEFAULT_INVALID_WORD_RULE

class AttrI18NWorker(BaseI18NWorker):
    #-------- HTML标签属性（仅处理‘文本’）处理 --------#
    worker_flag = 'attr'

    def extract(self, line_element, attr_list=ATTR_WORD_LIST):
        """
        提取html页面内自定义属性值ATTR_WORD_LIST 对应的翻译元素
        """
        word_list = []
        if 'start_tag' == line_element.e_type:
            line_element_tag_name = line_element.tag_name
            if 'base' == line_element_tag_name:  # 避免翻译_blank属性值
                return word_list
            tmp_attr_dict = line_element.attr_dict
            #-------- 处理搜索引擎的内容需要翻译  --------#
            if 'meta' == line_element_tag_name and tmp_attr_dict.has_key('name')\
                and tmp_attr_dict.has_key('content'):
                attr_dict_name_lower = tmp_attr_dict['name'].lower()
                if attr_dict_name_lower == 'description' or attr_dict_name_lower.startswith("xc_"):
                   word_list.append(tmp_attr_dict['content'])
                if attr_dict_name_lower == 'keywords':
                   word_list.extend(tmp_attr_dict['content'].split(",")) #  seo 仅以半角逗号分割
                return word_list
            if NOT_TRANS_TAG in tmp_attr_dict and tmp_attr_dict[NOT_TRANS_TAG] == ATTR_ON:
                return word_list
            word_list = [v for k,v in tmp_attr_dict.items() if v not in word_list and k in attr_list and v is not '']
        return word_list

    def integrate(self, line_element, words_dict, attr_list=ATTR_WORD_LIST):
        """
        译文替换, 在替换的过程中,进行判断是否需要进行替换.在此应用一些规则
        """
        if 'start_tag' == line_element.e_type:
            #属性翻译
            line_element_tag_name = line_element.tag_name
            if line_element_tag_name in IGNORE_TAG:
                #判断是否是可忽略的标签
                return line_element
            else:
                line_element_attr_dict = line_element.attr_dict
                #-------- SEO处理部分 --------#
                if 'meta' == line_element_tag_name and line_element_attr_dict.has_key('name')\
                    and line_element_attr_dict.has_key('content'):
                    tmp_attr_value = line_element_attr_dict['content']
                    attr_dict_name_lower = line_element_attr_dict['name'].lower()
                    if attr_dict_name_lower == 'description' or attr_dict_name_lower.startswith("xc_"):
                        line_element.update_attr('content', words_dict.get(tmp_attr_value,tmp_attr_value))
                        return line_element
                    if attr_dict_name_lower == 'keywords':
                        line_element.update_attr('content', merge_keywords(tmp_attr_value,words_dict))
                        return line_element
                for attr_kind in line_element_attr_dict:
                    if attr_kind not in attr_list or (NOT_TRANS_TAG in line_element_attr_dict and
                                                           line_element_attr_dict[NOT_TRANS_TAG] == ATTR_ON):
                        continue
                    tmp_attr_value = line_element_attr_dict[attr_kind]
                    if  words_dict.has_key(tmp_attr_value) and not re.match(DEFAULT_INVALID_WORD_RULE,tmp_attr_value):
                        line_element.update_attr(attr_kind, words_dict[tmp_attr_value])
        return line_element

    pass


def merge_keywords(content,words_dict):
    """
    SEO分词后的翻译合并
    :param content:
    :param words_dict:
    :return:
    """
    return ','.join([words_dict.get(item, item) for item in content.split(",")])
    pass