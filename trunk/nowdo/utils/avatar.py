# coding=utf-8
"""
created by SL on 14-4-2
"""
import hashlib
import urllib

__author__ = 'SL'


def get_avatar_url(email, size, default='identicon'):
    # construct the url
    # default_avatar_types = ['mm', 'retro', 'identicon', 'monsterid', 'wavatar']
    avatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(str(email).lower()).hexdigest() + "?"
    avatar_url += urllib.urlencode({'d': default, 's': str(size)})
    return avatar_url