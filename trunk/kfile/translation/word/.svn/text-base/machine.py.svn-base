# -*- coding: utf-8 -*-
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
import traceback
import eventlet.pools
import eventlet
#import opencc
# from apiclient.discovery import build
# from apiclient.errors import HttpError
#from ssl import SSLError
#from kfile.utils.req_wrap import stat
from kfile.utils.kfile_logging import logger
from Libs.sgmlparser.sgml.html_util import remove_all_blank
from kfile.utils.logger import random_logger
from kfile.translation.word.google_word_helper import GoogleWordHelper
from kfile.setting import GOOGLE_POOL_SIZE, GOOGLE_API_KEY
from kfile.translation.file.xml.xml_escape import unescape
from kfile.utils.zh import is_chinese

# eventlet.import_patched('apiclient.discovery')

googlePool = None
#microsoftPool = None #目前未使用


class Translator(object):
    def __init__(self):
        pass

    def build_translate_service(self):
        pass

    def translate(self, text, src_lang, tar_lang):
        pass


class GoogleTranslator(Translator):
    XC_2_G = {"cn": "zh-CN", "tw": "zh-TW"}
    agent_str = u"XXXXXXXXXX"


    def __init__(self):
        self.build_translate_service()
        super(GoogleTranslator, self).__init__()

    def build_translate_service(self):
        # self.service = build('translate', 'v2', developerKey=GOOGLE_API_KEY)
        pass


    def translate(self, text, src_lang, tar_lang):
        if src_lang == tar_lang:
            return text

        try:
            if src_lang in GoogleTranslator.XC_2_G:
                src_lang = GoogleTranslator.XC_2_G[src_lang]
            if tar_lang in GoogleTranslator.XC_2_G:
                tar_lang = GoogleTranslator.XC_2_G[tar_lang]

            src_lang = self.__get_decode(src_lang)
            tar_lang = self.__get_decode(tar_lang)
            text = self.__get_decode(text)
            #text = self.get_decode(self.str2utf8(text)[0])
            #print tar_lang, src_lang, text
            word_helper = GoogleWordHelper(text)
            kwargs = dict(target=tar_lang,
                q=word_helper.variable_free_origin)
            if src_lang:
                kwargs['source'] = src_lang
            content = self.service.translations().list(**kwargs).execute()
            result = self.__parse(content)
            result = word_helper.recover_variable(result)
            random_logger.debug("Google: <%s> from %s to %s: %s" % (text, src_lang, tar_lang, result))
            return result
        # except HttpError, e:
        #     logger.warn(traceback.format_exc(e))
        except Exception:
            logger.error("translate error.word is :%s and error info :%s" % (text, traceback.format_exc()))

        return None


    def __parse(self, content): #@ReservedAssignment
        result = None
        if len(content[u'translations']) == 1:
            ret = content[u'translations'][0][u'translatedText']
            if ret != '':
                result = ret

        if result:
            result = unescape(result, {'&quot;': '"', '&apos;': '\'', "&#39;": '\''})
        return result

    def __get_decode(self, content):
        try:
            if not isinstance(content, unicode):
                content = content.decode("utf-8")
        except Exception,e:
            import  chardet
            code_type = chardet.detect(content)
            logger.error("decode error. word is :%s and chardet :%s "%(content,code_type['encoding']))
        return content


import re

invalid_word = re.compile(r'[0-9./,:\-;+*%?!&$\(\)_#=~\'"@<>]+')

def translate_by_machine(word, src_lang, tar_lang, provider="google"):
    """
    word: 待翻译词条
    src_lang: 源语言
    tar_lang: 目标语言
    provider: 翻译服务提供商 如：google tranlation, microsoft bing
    """
    if src_lang == 'cn' and not is_chinese(word):
        return word

    #---- 无需翻译字符不过机器翻译 ----#
    tmp_word = remove_all_blank(word)
    tmp = invalid_word.sub('', tmp_word)
    if not tmp.strip(''):
        return word

    translator = __translate_by_google
    if provider == "microsoft":
        translator = __translate_by_microsoft
    if provider == "nocache":
        translator = __translate_by_google_no_cache

    #print 'Translating %s from %s to %s
    # %s' % (word, src_lang, tar_lang, provider)
    if src_lang == tar_lang:
        return word

    #每次翻译字数限制
    max_word_length = 200
    result = u""
    while True:
        short_word = word[:max_word_length]
        result += translator(short_word, src_lang, tar_lang) or u''
        if len(word) <= max_word_length:
            break
        word = word[max_word_length:]
    return result


def init_google_pool():
    """
    初始化google连接池
    :return: None
    """
    global googlePool
    if not googlePool:
        try:
            googlePool = eventlet.pools.Pool(min_size=GOOGLE_POOL_SIZE,
                max_size=GOOGLE_POOL_SIZE, create=lambda: GoogleTranslator())
        except Exception, e:
            logger.error(traceback.format_exc())

#opencc_s2t = opencc.OpenCC('s2t')
#opencc_t2s = opencc.OpenCC('t2s')

def __translate_by_google(word, src_lang, tar_lang):
    # 如果是中文且裏面沒
    from kfile.controls.word_cache import WordCache
    from kfile.controls.session import word_cache_sessionCM

    with word_cache_sessionCM() as session:
        #机器翻译缓存查询, 此处默认md5是唯一的
        word_cache = WordCache.get(session, word, src_lang, tar_lang)
        if word_cache:
            random_logger.debug("WordCache: <%s> from %s to %s: %s" % (word, src_lang, tar_lang, word_cache.target))
            return word_cache.target
        else:
            #if src_lang == 'cn' and tar_lang == 'tw':
            #   result = opencc_s2t.convert(word)
            #elif src_lang == 'tw' and tar_lang == 'cn':
            #   result = opencc_t2s.convert(word)
            #else:
            result = __translate_by_google_no_cache(word, src_lang, tar_lang)
            #把查询结果插入缓存
            if result:
                WordCache.add(session, word, src_lang, tar_lang, result)
            return result


def __translate_by_google_no_cache(word, src_lang, tar_lang):
    """
    :param word: 词汇
    :param src_lang: 原始语言
    :param tar_lang: 目标语言
    :return: 翻译后的词汇或None(查不到)
    """

    init_google_pool()

    result = None
    with googlePool.item() as translator:
        for i in range(2): # 当长时间不适用google翻译时，连接可能失效。所以重试一次。
            try:
                result = translator.translate(word, src_lang, tar_lang)
            except Exception, e:
                logger.error(traceback.format_exc())
                translator.build_translate_service()
            if result:
                return result
        return None


def __translate_by_microsoft(word, src_lang, tar_lang):
    pass

if __name__ == '__main__':
    #session = get_default_session()
    #insert_langs(session)
    #session.close()
    #print translate_by_machine(u"BAB'S BOUTIQUE", 'en', 'pt')
    #print '-----------'
    #print translate_by_machine(u"我是中国人", 'cn', 'en')
    #print '-----------'
    #print '结果',translate_by_machine(u"I am a girl!", 'en', 'cn')
    #print '-----------'
    #print translate_by_machine(u"I am a girl!", 'en', 'pt')
    #print '-----------'
    #print translate_by_machine(u"古代遗迹3-119", 'cn', 'tw')
    #print translate_by_machine(u"3-119", 'cn', 'tw')
    print translate_by_machine(u"軟體乾隆乾淨", 'tw', 'cn')
    print translate_by_machine(u"软件乾隆干净", 'cn', 'tw')
    #test_translate_by_machine(10)
