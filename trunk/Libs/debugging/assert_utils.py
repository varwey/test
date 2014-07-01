# -*- coding: utf-8 -*-

"""
assert 函数调用次数
"""
__author__ = 'yeshiming@gmail.com'

from threading import RLock
_time_dict = {}

_lock = RLock()

def count_time(func):

    def new_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        print 'fucccc'
        with _lock:
            _time_dict[func] = _time_dict.get(func, 0) + 1
        return ret
    return new_func

def get_time_cnt(func):
    return _time_dict.get(func, 0)

