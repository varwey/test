# coding=utf-8
"""
created by SL on 14-3-7
"""
import string
import random
import datetime
import time

__author__ = 'SL'


def get_random_key():
    return ''.join([random.choice(string.letters) for i in xrange(48)])


def get_random_filename():
    return ''.join([random.choice(string.letters) for i in xrange(5)]) + str(time.time())[:-3]

if __name__ == '__main__':
    print get_random_key()
    print datetime.time()
    print str(time.time())[:-3]
    print get_random_filename()