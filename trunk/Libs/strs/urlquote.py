# -*- coding: utf-8 -*-

import re
import traceback
from urllib import quote


__author__ = 'yeshiming@gmail.com'


_encode_pat = re.compile(r"%[0-9a-f]{2}", re.IGNORECASE)


def xc_quote(url):
    """
    :param url: should have scheme://
    只处理url中的path部分;
    不处理问号(?)以后的query string;
    """
    try:
        _encoded = url.split("/", 3)[3]
        _untouch = url[0: len(url) - len(_encoded)]
        assert _untouch + _encoded == url
        _end_untouch = "".join(url.partition("?")[1:3])
        _encoded = _encoded[0: len(_encoded) - len(_end_untouch)]
        assert _untouch + _encoded + _end_untouch == url
        if not re.search(_encode_pat, _encoded):
            return _untouch + quote(_encoded, safe="/~") + _end_untouch
    except IndexError:
        pass
    except AssertionError:
        print traceback.format_exc()
        print "url: %s"%url

    return url



if __name__ == '__main__':
    one_of_unknown_str_ = xc_quote("http://trello.com/board/backend/4f54d53530c3%208f530892d8b0")
    print one_of_unknown_str_

    assert xc_quote("http://trello.com/board/backend/4f54d53530c3 8f530892d8b0") == one_of_unknown_str_
    assert xc_quote("http://trello.com/board/backend/4f54d53530c3%208f530892d8b0") == "http://trello.com/board/backend/4f54d53530c3%208f530892d8b0"
    assert xc_quote("https://trello.com/board/backend/4f54d53530c3%208f530892d8b0?dsfijo?dsfgd") == "https://trello.com/board/backend/4f54d53530c3%208f530892d8b0?dsfijo?dsfgd"
    assert xc_quote("https://t.sdfsdf.sdfasdf.asdfadf.asdrello.com/board/backend/4f54d53530c3") == "https://t.sdfsdf.sdfasdf.asdfadf.asdrello.com/board/backend/4f54d53530c3"
    assert xc_quote("http://f.xingcloud.com/tdsheep/tw/app16488.imgcache.qzoneapp.com/app16488/static/images/swf/TDSheepMain.swf?version=20130129_001") == "http://f.xingcloud.com/tdsheep/tw/app16488.imgcache.qzoneapp.com/app16488/static/images/swf/TDSheepMain.swf?version=20130129_001"
    assert xc_quote("http://f.xingcloud.com/tdsheep/tw/app16488.imgcache.qzoneapp.com/app16488/static/images/swf/TDSheepMain.swf?%s=5A") == "http://f.xingcloud.com/tdsheep/tw/app16488.imgcache.qzoneapp.com/app16488/static/images/swf/TDSheepMain.swf?%s=5A"
    assert xc_quote("http://f.xingcloud.com/tdsheep/tw/app16488.imgcache.qzoneapp.com/app16488/static/images/swf/TDSheepMain.swf?") == "http://f.xingcloud.com/tdsheep/tw/app16488.imgcache.qzoneapp.com/app16488/static/images/swf/TDSheepMain.swf?"
    assert xc_quote("http://app16488.imgcache.qzoneapp.com/app16488/static/images/swf/gameUI/loading_tw.swf?v=20130129_001") == "http://app16488.imgcache.qzoneapp.com/app16488/static/images/swf/gameUI/loading_tw.swf?v=20130129_001"

    assert xc_quote("http://www.baidu.com") == "http://www.baidu.com"
    assert xc_quote("http://10.1.15.197:8077") == "http://10.1.15.197:8077"
    assert xc_quote("http://10.1.15.197:8077/") == "http://10.1.15.197:8077/"
