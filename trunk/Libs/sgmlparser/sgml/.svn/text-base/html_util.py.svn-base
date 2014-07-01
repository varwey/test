# coding=utf-8
'''
Created on 2011-12-27

@author: Admin
'''

import re
from Libs.strs.coding_util import get_unicode


replace_dict = {"&apos;":"'","&#39;":"'",
                "&quot;":'''"''',"&#34;":'''"'''}
def unescape(data):
    try:
        for key, value in replace_dict.items():
            data = data.replace(key, value)
        
        # must do "&" last
        data = data.replace("&amp;", "&")
        data = data.replace("&#38;", "&")
    except AttributeError:
        pass
    return data

import codecs
def trim_bom(_str):
    """
    移除bom头
    :param _str:
    :return: (头,str) "%s%s"% return_result  为源字符串
    """
    if not _str:
        return '',_str
    if len(_str) < 3:
        return '',_str
    if _str[:3] == codecs.BOM_UTF8:
        return codecs.BOM_UTF8,_str[3:]
    return '',_str

def str2utf8(stri, encoding = None):
    if isinstance(stri, unicode):
        try:
            return stri.encode('utf8'), "unicode"
        except:
            pass

    try:
        if encoding:
            return stri.decode(encoding).encode('utf8'),encoding
        else:
            raise Exception()
    except:
        for c in ('utf8', 'shift-jis', 'euc-jp', 'gbk', 'iso-8859-1', 'utf16','utf32','gb2312'):
            try:
                return stri.decode(c).encode('utf8'),c
            except:
                pass
    return stri,""


reg_replace_white_space_obj = re.compile('\s*')

def remove_all_blank(content):
    tmp_content = content
    tmp_content = remove_nbsp(tmp_content)
    tmp_content = re.sub(reg_replace_white_space_obj, '', tmp_content)
    return tmp_content

def remove_nbsp(content):
    #移除html中空格符表示字符串：&nbsp;
    tmp_content = content
    content = get_unicode(content)
    try:
        if isinstance(content, unicode):
            content = content.replace(u'\u00a0', '').encode('utf8')
            return content
        else:
            return content
    except:
        return tmp_content


class ReplacedObject:
    def __init__(self):
        self.rp_num = 0
        self.rp_dict = {}

    def replace(self, matchobj):
        if matchobj.group(2).strip():
            self.rp_num += 1
            temp_s = "<%s>XCXCXCXCXCXCXCXCX%s</%s>" % (matchobj.group(1), self.rp_num, matchobj.group(3))
            self.rp_dict[temp_s] = matchobj.group(0) #repr(matchobj.group(0)).strip('\'\"')
        else:
            temp_s = matchobj.group(0)
        return temp_s

js_pattern = re.compile("<(script.*?[^/]?)>([\S\s]*?)</(script)>",flags=re.IGNORECASE)
def html_jsscript_extract(content):
    '''对内容进行预处理，将所有的js代码滤出，使得不影响lxml的解析'''
    tmp_object = ReplacedObject()
    content = re.sub(js_pattern, tmp_object.replace, content)
    return content, tmp_object.rp_dict

cs_pattern = re.compile("<(style.*?[^/]?)>([\S\s]*?)</(style)>",flags=re.IGNORECASE)
def html_css_extract(content):
    '''对于style中直接编写的css 替换掉'''
    tmp_object = ReplacedObject()
    content = re.sub(cs_pattern, tmp_object.replace, content)
    return content, tmp_object.rp_dict


def html_replace_integrate(content, script_rule):
    for rule in script_rule:
        content = content.replace(rule, script_rule[rule])
    return content

charset_compile = re.compile("<meta[^>]*?charset.*?>")
def modify_meta_charset2utf8(content):
    return re.sub(charset_compile,'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',content)


filter_trans = re.compile("<i>[\S\s]*?</i>\s*?<b>([\S\s]*?)</b>")
class EffectiveTrans():
    def __init__(self):
        self.trans_result = ''

    def replace(self, matchobj):
        if matchobj.group(1):
            self.trans_result += matchobj.group(1)
            return ''
        else:
            return matchobj.group(0)

def filter_trans_result(result_str):
    #过滤可能由于google翻译出错：a--><i>a</i><b>a'</b>的结果
    if not re.search(filter_trans, result_str):
        return result_str
    effective_trans = EffectiveTrans()
    re.sub(filter_trans, effective_trans.replace, result_str)
    return effective_trans.trans_result

import lxml.html.soupparser
from lxml import etree
import traceback
from Libs.sgmlparser.constant import NOT_TRANS_TAG, ATTR_ON
#TMP_TAG = "XCXCXCXCXCXCXCXC"

class FragmentExtract(object):
    def __init__(self, content):
        self.content = content

    def extract(self):
        tag = self._extract_tag()
        text = self._extract_text()
        return (tag, text)

    def _extract_text(self):
        return self.content

    def _extract_tag(self):
        return ''

    @classmethod
    def integrate(cls, tag, text, translate = False, visible = True):
        if not visible:
            return ''
        else:
            content = text
            if translate:
                return content
            else:
                try:
                    doc = lxml.html.soupparser.fromstring(content).getchildren()[0]
                    doc.set(NOT_TRANS_TAG, ATTR_ON)
                    return etree.tostring(doc, encoding='utf-8', pretty_print=False, method='html')
                except :
#                    logger.warning('The local fragment integrate error : %s.'%traceback.format_exc())
                    return ''
            pass
        pass

from urlparse import urlparse, urlunparse
def generate_src_uri(project_info, xc_uri):
    #src_url_parts = 'http://www.focalprice.com'
    #dst_url_parts = 'http://usi.xingcloud.com/en/show/12345667/?Cate=Hot'
    #               || 'http://pt.focalprice.com/en/show/12345667/?Cate=Hot'
    #result = 'http://www.focalprice.com/en/show/12345667/?Cate=Hot'
    src_host = project_info.src_host
    src_url_parts = urlparse(src_host)
    dst_url_parts = urlparse(xc_uri)
    return urlunparse((dst_url_parts.scheme, src_url_parts.netloc, dst_url_parts.path, dst_url_parts.params,
        dst_url_parts.query, dst_url_parts.fragment))
    pass


if __name__=="__main__":
    pass
