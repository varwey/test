#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# author = "hhl"

try:
    from PIL import Image
except ImportError:
    import Image

import string
import random


class EntryListException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def gen_random_name():
    return string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l'], 12)).replace(" ", "")

def rm_braces(str):
    index = str.find('}')
    return str[index+1:]

def get_seqRun_content_rel(str):
    word_dict = {}
    if len(str)== 0 :
        return word_dict

    if str.find('{') < 0:
        return {"0": str}

    str = str.lstrip()
    if str[0] != '{':
        return word_dict
    temp_str = str
    index = 1
    while True:
        right_index = temp_str.find('}')
        # print "temp_str =",temp_str, "right_index:", right_index
        seq = temp_str[1:right_index]
        index = temp_str[right_index:].find('{')
        # print "index =", index
        if index<0:
            word_dict[seq] = temp_str[right_index+1:]
            break
        else:
            word_dict[seq] = temp_str[right_index+1:right_index+index]
            temp_str = temp_str[right_index+index:]
            # print temp_str

    return word_dict


def content_to_stringIO(file_path= None, file_contents=None):
    if file_path is None and file_contents is None:
        raise Exception("file error ,please input file path or file_contents")
    if file_path:
        file = file_path
    else:
        from cStringIO import StringIO
        file = StringIO(file_contents)

    return file