# coding=utf-8
"""
created by SL on 14-3-31
"""
import re

__author__ = 'SL'


def strip_tags(html_str, exclude=None):
    add_line_end_re = re.compile(r'(<\/p[^>]*>|<\/div[^>]*>|<br\/?>)')
    striptags_re = re.compile(r'<!--.*?-->|<[^>]*>')
    if not exclude:
        return striptags_re.sub('', add_line_end_re.sub('\g<1>\n', html_str))
    else:
        exclude_re = re.compile(exclude)
        print html_str
        matched_tags = exclude_re.findall(html_str)
        print matched_tags
        split_tags = exclude_re.split(html_str)

        res = ''
        for index, t in enumerate(split_tags):
            res += str(strip_tags(t))
            if len(matched_tags) > index:
                res += matched_tags[index]
        return res


def escape(string):
    return string.replace('&', '&amp;')\
        .replace('>', '&gt;')\
        .replace('<', '&lt;')\
        .replace("'", '&#39;')\
        .replace('"', '&#34;')


def escape_tags_exclude(html_str, exclude=None):
    """
    对 exclude 以外的内容进行 escape
    """
    if not exclude:
        return escape(html_str)
    exclude_re = re.compile(exclude)

    matched_tags = exclude_re.findall(html_str)
    split_tags = exclude_re.split(html_str)

    res = ''
    for index, t in enumerate(split_tags):
        res += str(escape(t))
        if len(matched_tags) > index:
            res += matched_tags[index]
    return res


def escape_tags_include(html_str, include=None):
    """
    对 include 匹配的内容进行 escape
    """
    if not include:
        return escape(html_str)
    include_re = re.compile(include)

    matched_tags = include_re.findall(html_str)
    split_tags = include_re.split(html_str)

    res = ''
    for index, t in enumerate(split_tags):
        res += t
        if len(matched_tags) > index:
            res += str(escape(matched_tags[index]))
    return res


def deal_topic_content(html_str):
    if not html_str:
        return ''
    return escape_tags_exclude(html_str, r'</?p.*?>|</?a.*?>|<img.*?/?>|<br/?>')


def deal_task_content(html_str):
    if not html_str:
        return ''
    tag_stripped_str = strip_tags(html_str, r'</?p.*?>|</?a.*?>|<img.*?/?>|<br/?>')
    style_re = re.compile(r'(?<=\s)style=[\'\"][^>\'\"]*?[\'\"](?=\s|>)', re.I)
    return style_re.sub('', tag_stripped_str)


def escape_unsafe_content(html_str):
    if not html_str:
        return ''
    return escape_tags_include(html_str, r'</?script.*?>')


def filter_images(html_str):
    """
    从html内容中过滤出图片标签，返回图片数组
    """
    img_tag_re = re.compile(r'<img [^>]*?src=[\'\"](.*?)[\'\"][^>]*?>', re.I)
    # img_tag_re = re.compile(r'<img[^>]*>')
    return img_tag_re.findall(html_str)


def strip_images(html_str):
    """
    过滤掉图片标签
    """
    img_tag_re = re.compile(r'<img [^>]*?src=[\'\"](.*?)[\'\"][^>]*?>', re.I)
    # img_tag_re = re.compile(r'<img[^>]*>')
    return img_tag_re.sub("", html_str)

if __name__ == '__main__':
    html_str_test = u'<p><script>alert("hello world!");</script></p><p><h1>11111H1</h1></p><p>22222</p><p>' \
                    u'<img src="www.baidu.com/a.jpg" style="width: 71px;"><br></p><p></p><p>' \
                    u'<img src="www.baidu.com/b.jpg" style="width: 72px;">' \
                    u'<img src="www.baidu.com/c.jpg" style="width: 73px;">' \
                    u'<img src="www.baidu.com/c.jpg" style="height: 99px;">' \
                    u'<img src="www.baidu.com/d.jpg" style="width: 74px;">' \
                    u'<h2 style="width: 75px;"> style="width: 222222px;" </h2>' \
                    u'<a href="http://www.timefly.cn">33333</a></p>'
    # print escape_tags(html_str_test)
    # print deal_topic_content(html_str_test)
    # print strip_tags(html_str_test)
    # print filter_images(html_str_test)
    # print html_str_test
    # print strip_images(html_str_test)
    print deal_task_content(html_str_test)