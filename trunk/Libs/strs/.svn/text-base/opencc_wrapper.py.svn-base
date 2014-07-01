#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import cast, cdll, c_char_p, c_int, c_size_t, c_void_p, CDLL
from ctypes.util import find_library
import sys
import os
import chardet
from Libs.strs.coding_util import str2utf8


class ConvertError(Exception):
    pass

class DictType:
    TEXT,DATRIE = 0,1

class OpenCC:

    def __init__(self, config=None, verbose=True):
#        self.libopencc = cdll.LoadLibrary(find_library('opencc'))
        self.libopencc = cdll.LoadLibrary("libopencc.so.1")

        self.libopencc.opencc_open.restype = c_void_p
        self.libopencc.opencc_convert_utf8.argtypes = [c_void_p, c_char_p, c_size_t]
        # for checking for the returned '-1' pointer in case opencc_convert() fails.
        # c_char_p always tries to convert the returned (char *) to a Python string,
        self.libopencc.opencc_convert_utf8.restype = c_void_p
        self.libopencc.opencc_close.argtypes = [c_void_p]
        self.libopencc.opencc_perror.argtypes = [c_char_p]
        self.libopencc.opencc_dict_load.argtypes = [c_void_p, c_char_p, c_int]

#        self.libc = cdll.LoadLibrary(find_library('c'))
        self.libc = cdll.LoadLibrary("libc.so.6")
        self.libc.free.argtypes = [c_void_p]

        self.config = config
        self.verbose = verbose
        self.od = None
#        if self.config is None:
#            self.od = self.libopencc.opencc_open(0)
#        else:
#            self.od = self.libopencc.opencc_open(c_char_p(self.config))
    
    def __enter__(self):
        if self.config is None:
            self.od = self.libopencc.opencc_open(0)
        else:
            self.od = self.libopencc.opencc_open(c_char_p(self.config))
        return self

    def __exit__(self, type, value, traceback):
        self.libopencc.opencc_close(self.od)
        self.od = None

    def __perror(self, message):
        if self.verbose:
            self.libopencc.opencc_perror(message)
    
    def convert(self, text):
        retv_c = self.libopencc.opencc_convert_utf8(self.od, text, len(text))
        if retv_c == -1:
            self.__perror('OpenCC error:')
            raise ConvertError()
        retv_c = cast(retv_c, c_char_p)
        str_buffer = retv_c.value
        self.libc.free(retv_c);
        return str_buffer
    
    def dict_load(self, filename, dicttype):
        retv = self.libopencc.opencc_dict_load(self.od, filename, dicttype)
        if retv == -1:
            self.__perror('OpenCC error:')
        return retv


def _opencc(config, entry_word):
    """
        @param config: 's2t' -- simple to traditional
                           't2s' -- traditional to simple
        @param entry_word: the word to be translated
    """
    config_list = []
    if config == 's2t':
        config_list += ['simp_to_trad_characters.ocd', 
                            'simp_to_trad_phrases.ocd']
    elif config == 't2s':
        config_list += ['trad_to_simp_characters.ocd', 
                           'trad_to_simp_phrases.ocd']
            
    with OpenCC() as converter:
        for path in config_list:
            converter.dict_load(path, DictType.DATRIE)
        return converter.convert(entry_word)


def opencc(config, entry_word):
    try:
        # 调用 _opencc
        result = _opencc(config, str2utf8(entry_word)[0])
    except:
        import traceback
        print traceback.format_exc()
        return entry_word
    # 返回
    return result

#opencc_instance = OpenCC()

#opencc_s2t = OpenCC()
#opencc_t2s = OpenCC()

#def init():
#    for path in ['simp_to_trad_characters.ocd',
#                 'simp_to_trad_phrases.ocd']:
#        opencc_s2t.dict_load(path, DictType.DATRIE)
#        
#    for path in ['trad_to_simp_characters.ocd', 
#                'trad_to_simp_phrases.ocd']:
#        opencc_t2s.dict_load(path, DictType.DATRIE)

if __name__ == "__main__":
    
#    with sys.stdin as fp:
#        text = fp.read()
#    with OpenCC() as converter:
#        for path in ['simp_to_trad_characters.ocd',
#                 'simp_to_trad_phrases.ocd']:
#            converter.dict_load(path, DictType.DATRIE)
#        print converter.convert(text)
    test_word1 = "恶魔卡"
    chardet.detect(test_word1)
    test_word2 = "我們是祖國美麗的花朵，乾隆乾淨軟體"
    print opencc('s2t', test_word1)
    print opencc('t2s', test_word2)
#    print opencc_instance.opencc('s2t', test_word1)
    
#    init()
#
#    print opencc_s2t.convert(test_word1)
#    print opencc_t2s.convert(test_word2)
#    print opencc_s2t.convert(test_word1)
#    print opencc_t2s.convert(test_word2)

