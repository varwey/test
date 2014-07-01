# -*- coding: utf-8 -*-
__author__ = 'yeshiming@gmail.com'

import re
_pat = re.compile(r'[a-fA-F0-9]{15,}')
_has_number = re.compile(r'[0-9]+')


def is_hash(s):
    return re.match(_pat, s) and re.search(_has_number, s) is not None


if __name__ == '__main__':
    assert not is_hash("modification")
    assert is_hash("99aed01d9a8a460e845696cc103156cf9922b84cd2a4168fb4465552c5037be3a60a429c4497d089279f88f5cdacd957")
    assert not is_hash("Wholesale - Natural Emerald Stretch Bracelet Round Loose beads 11mm 02219")