# -*- coding=utf-8 -*-
from nowdo.config import setting

__author__ = 'zou'


def supported_languages(**kwargs):
    languages = {}
    with_short = kwargs.get('with_short', None)
    for lang, value in setting.SUPPORTED_LANGUAGES_FULL.items():
        if with_short:
            languages[lang] = ''.join(['[', lang.upper(), '] ', value['name']])
        else:
            languages[lang] = value['name']
    return languages


def supported_languages_full():
    return setting.SUPPORTED_LANGUAGES_FULL


def sorted_supported_languages_tuples(**kwargs):
    res = []
    lang = supported_languages()
    for k in sorted(lang.keys(), key=lambda x: x):
        item = (k, lang.get(k))
        if kwargs.get('with_short'):
            item = (k, ''.join(['[', k.upper(), '] ', lang.get(k)]))
        res.append(item)

    return res

