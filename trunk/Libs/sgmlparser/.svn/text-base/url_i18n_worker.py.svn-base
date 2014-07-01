# coding=utf8
'''
Created on Aug 20, 2012

@author: harveyang
'''

from Libs.sgmlparser.base_i18n_worker import BaseI18NWorker
from Libs.sgmlparser.constant import ATTR_LINK_LIST


class UrlI18NWorker(BaseI18NWorker):
    #------ HTML URL 处理 -----#
    worker_flag = 'url'

    def extract(self, line_element, attr_list=ATTR_LINK_LIST):
        """
        只提取特定属性的值
        :param line_element:
        :param attr_list:
        :return: link list
        """
        link_list = []
        if 'start_tag' == line_element.e_type:
            link_list = [v for k,v in line_element.attr_dict.items()\
                         if v not in link_list and k.lower() in attr_list]
        return link_list
        pass

    def integrate(self, line_element, links_dict , attr_list=ATTR_LINK_LIST):
        """
        url 替换
        :param line_element:
        :param links_dict:
        :param attr_list:
        :return:
        """
        attr_dict = line_element.attr_dict
        if 'start_tag' == line_element.e_type and len(attr_dict):
            for k, v in attr_dict.items():
                if k in attr_list and not v.startswith('javascript:') and links_dict.has_key(v) :
                    line_element.update_attr(k, links_dict[v])
        return line_element
        pass


