#coding=utf8
from Libs.sgmlparser.sgml.html_util import str2utf8
from Libs.strs.opencc_wrapper import opencc
__author__ = 'T510'

import re

unicode_encoding_dict = {
    "cjk": re.compile(u"[\u4E00-\u9FFF]+", re.UNICODE),
    "en": re.compile(ur"[\u0061-\u007a]+|[\u0041-\u005a]+", re.UNICODE),
    "number": re.compile(ur"[\u0030-\u0039]", re.UNICODE),
    "ja": re.compile(ur"[\u3040-\u30FF]+|[\u3104-\u312A]+|[\uFF66-\uFF9E]+", re.UNICODE),
    "ko": re.compile(ur"[\u1100-\u11F9]+|[\u3130-\u318E]+|[\uAC00-\uD7A3]+", re.UNICODE),
    "ar": re.compile(ur"[\u0600-\u06FF]+|[\u0750-\u077F]+|[\u08A0-\u08FF]+|[\uFB50-\uFDFF]+|[\uFE70-\uFEFF]+", re.UNICODE),
    "ru": re.compile(ur"[\u0400-\u052F]+", re.UNICODE),
    }


detect_switch = {
    'cn': lambda data: _unicode_cn(data),
    'tw': lambda data: _unicode_tw(data),
    'en': lambda data: _unicode_en(data),
    'ru': lambda data: _unicode_ru(data),
    'ko': lambda data: _unicode_ko(data),
    'ja': lambda data: _unicode_ja(data),
    'ar': lambda data: _unicode_ar(data),
}


def unicode_detect_language(data, lang):
    '''
    @param data: 待检测数据data
    @param lang: 待检测语言
    @return: 检测结果 true or false
    '''
    if lang == 'zh-CN': lang = 'cn'
    if lang == 'zh-TW': lang = 'tw'

    if detect_switch.has_key(lang):
        return detect_switch[lang](data)
    else:
        return True


def _unicode_cn(data):
    '''
    @param data: unicode data
    @return: 检测结果 true or false
    '''
    if _unicode_cjk(data):
        return _opencc_detect(data, 'cn')
    else:
        return False


def _unicode_tw(data):
    '''
    @param data: unicode data
    @return: 检测结果 true or false
    '''
    if _unicode_cjk(data):
        return _opencc_detect(data, 'tw')
    else:
        return False
    pass


def _opencc_detect(data, lang):
    '''
    @param data: 待检测数据data
    @param lang: 待检测语言
    @return: 检测结果 true or false
    '''
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    if lang in ['tw']:
        result = opencc('s2t', data)
    else:
        result = opencc('t2s', data)
    return data == result


def _unicode_cjk(data):
    '''
    判断是否是中文，不区分简，繁
    @param data:  unicode data
    @return:  检测结果 True or False
    '''
    return _unicode_language(data, 'cjk', 0.5)


def _unicode_en(data):
    '''
    @param data:  unicode data
    @return:  检测结果
    '''
    return _unicode_language(data, 'en', 0.6)


def _unicode_ja(data):
    '''

    @param data: unicode data
    @return: 检测结果（true or false）
    '''
    return _unicode_language(data, 'ja', 0.5)

def _unicode_ko(data):
    '''
    @param data:  unicode data
    @return: 检测结果（true or false）
    '''
    return _unicode_language(data, 'ko', 0.5)


def _unicode_ar(data):
    '''
    @param data: unicode data
    @return: 检测结果（true or false）
    '''
    return _unicode_language(data, 'ar', 0.6)


def _unicode_ru(data):
    '''
    @param data: unicode data
    @return: 检测结果 True 偶然 False
    '''
    return _unicode_language(data, 'ru', 0.6)


def _unicode_language(data, lang, scale):
    '''
    @param data: unicode data
    @param lang:  语言
    @param scale: 比重因子
    @return: 检测结果（true or false）
    '''
    if not data:
        #空字符串被认为是任何语言
        return True
    if not isinstance(data, unicode):
        try:
            data = str2utf8(data)[0].decode('utf-8')
        except:
            #不识别的类型认为是给定的类型
            return True
    f_data_list = re.findall(unicode_encoding_dict[lang], data)
    if len(''.join(f_data_list)) / float(len(data)) > scale:
        return True
    else:
        return False


def test():
    assert _unicode_cjk(u'爱你')
    assert not _unicode_cjk(u'ウェブ')
    assert _unicode_ja(u'ウェブ')
    assert not _unicode_cjk(u' 송진원 기자 = 검찰이 불법 정치자금 6천만원을 받은 혐의로 중앙선')


if __name__ == "__main__":
    test()
    text = u'I love you for ever!'
    print _unicode_cjk(text)
    print _unicode_en(text)
    print '111', _unicode_ja(u'ウェブ')
    print '2222', _unicode_ko(u' 송진원 기자 = 검찰이 불법 정치자금 6천만원을 받은 혐의로 중앙선')
    print _unicode_ar(u"مرحبا")
    print '-------------------'
    print unicode_detect_language("微博", 'cn')
    print unicode_detect_language("微博", 'tw')
    print unicode_detect_language("寶貝", 'cn')
    print unicode_detect_language(u"寶貝", 'cn')
    print unicode_detect_language(u"寶貝", 'tw')
    print _unicode_cn("寶貝")
    print _unicode_tw("寶貝")