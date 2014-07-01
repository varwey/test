# coding=utf8

"""
url normalization
"""
import re
import urlparse


def format_url(url):
    new_url = lower_domain(url)
    return remove_duplicate_slash(new_url)


def lower_domain(url):
    '''
    URL 域名小写 转换
    @param url: 待处理的连接 URL
    @return: 返回域名小写的URL
    '''
    lower_url = url.lower()
    if lower_url.startswith('http://') or lower_url.startswith('https://') or lower_url.startswith('//'):
        url_parts = urlparse.urlparse(url)
        if url_parts.scheme:
            url = url.replace(url[:len(url_parts.scheme)], url_parts.scheme, 1)
        return url.replace(url_parts.netloc, url_parts.netloc.lower(), 1)
    else:
        return url


def remove_duplicate_slash(url):
    """
    去除url的path中连续出现的"/"
    :param url:
    :return:
    """
    pre, qm, qs = url.partition("?")

    parse_result = urlparse.urlparse(pre)
    if parse_result.scheme:
        pos = len(parse_result.scheme) + 3
    elif url.startswith('//'):
        pos = 2
    else:
        pos = 0

    head = pre[0:pos]
    tail = pre[pos:]
    new_tail = re.sub(r"/{2,}", "/", tail)

    return head + new_tail + qm + qs



if __name__ == "__main__":
    assert remove_duplicate_slash('http://www.example.com//') == 'http://www.example.com/'
    assert remove_duplicate_slash('http://www.example.com///') == 'http://www.example.com/'
    assert remove_duplicate_slash('http://www.example.com/foo//bar.html') == 'http://www.example.com/foo/bar.html'
    assert remove_duplicate_slash('http://www.example.com/?key=//') == 'http://www.example.com/?key=//'
    assert remove_duplicate_slash('http://www.example.com/?key=foo//') == 'http://www.example.com/?key=foo//'

    assert remove_duplicate_slash('//www.example.com//') == '//www.example.com/'
    assert remove_duplicate_slash('www.example.com//') == 'www.example.com/'
    assert remove_duplicate_slash('www.example.com///') == 'www.example.com/'
    assert remove_duplicate_slash('www.example.com/foo//bar.html') == 'www.example.com/foo/bar.html'
    assert remove_duplicate_slash('www.example.com/?key=//') == 'www.example.com/?key=//'
    assert remove_duplicate_slash('www.example.com/?key=foo//') == 'www.example.com/?key=foo//'

    assert format_url("HTTP://www.baidu.com//a.html") == 'http://www.baidu.com/a.html'
    assert format_url("HTTPS://www.baidu.com//") == 'https://www.baidu.com/'

    from contextlib import closing

    with closing(open('E:\\filenames.txt', 'rb')) as f:
        for line in f.readlines():
            source = line.strip()
            try:
                assert remove_duplicate_slash(source) == source
            except AssertionError:
                print source, remove_duplicate_slash(source)