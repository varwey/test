# -*- coding: utf-8 -*-

"""
词汇个数统计
此模块定义了三种字符：
1. 不计费的分隔符。只有分割作用，如标点符号。
2. 计费的分割符。既有分割作用，每个算一个计费单位。
3. 非分隔符。无分割作用，多个连续的非分隔符算一个计费单位。

此模块枚举所有分隔符的unicode段，剩下的全是非分隔符。
如果发现wordcnt对某些字符处理不正确，一般只需调整sep_range 和 pay_range的元素。
"""


__author__ = 'yeshiming@gmail.com'

import re


# 以下数据来源
# http://zh.wikipedia.org/wiki/Unicode%E5%AD%97%E7%AC%A6%E5%B9%B3%E9%9D%A2%E6%98%A0%E5%B0%84#.E7.AC.AC.E4.B8.80.E8.BC.94.E5.8A.A9.E5.B9.B3.E9.9D.A2

# 枚举所有分隔符(包括计费分隔符和不计费分隔符)的unicode段，剩下的全是非分隔符
sep_range = """
0000-001F   C0控制符    C0 Controls
0020-0020   空格
0080-009F   C1控制符    C1 Controls
00A0-00BF   拉丁文扩充中的符号
0250-02AF   国际音标扩展    IPA Extensions
02B0-02FF   占位修饰符号    Spacing Modifiers
0300-036F   结合附加符号    Combining Diacritics Marks
19E0-19FF   高棉文符号  Khmer Symbols
1DC0-1DFF   结合附加符号补充    Combining Diacritics Marks Supplement
2000-206F   常用标点    General Punctuation
2070-209F   上标及下标  Superscripts and Subscripts
20A0-20CF   货币符号    Currency Symbols
20D0-20FF   组合用记号  Combining Diacritics Marks for Symbols
2100-214F   字母式符号  Letterlike Symbols
2190-21FF   箭头    Arrows
2200-22FF   数学运算符  Mathematical Operator
2300-23FF   杂项工业符号    Miscellaneous Technical
2440-245F   光学识别符  Optical Character Recognition
2500-257F   制表符  Box Drawing
2600-26FF   杂项符号    Miscellaneous Symbols
2700-27BF   印刷符号    Dingbats
27C0-27EF   杂项数学符号-A  Miscellaneous Mathematical Symbols-A
27F0-27FF   追加箭头-A  Supplemental Arrows-A
2900-297F   追加箭头-B  Supplemental Arrows-B
2980-29FF   杂项数学符号-B  Miscellaneous Mathematical Symbols-B
2A00-2AFF   追加数学运算符  Supplemental Mathematical Operator
2B00-2BFF   杂项符号和箭头  Miscellaneous Symbols and Arrows
2E00-2E7F   追加标点    Supplemental Punctuation
2E80-2EFF   中日韩部首补充  CJK Radicals Supplement
2FF0-2FFF   表意文字描述符  Ideographic Description Characters
3000-303F   中日韩符号和标点    CJK Symbols and Punctuation
3190-319F   象形字注释标志  Kanbun
31C0-31EF   中日韩笔画  CJK Strokes
3200-32FF   带圈中日韩字母和月份    Enclosed CJK Letters and Months
3300-33FF   中日韩兼容  CJK Compatibility
3400-4DBF   中日韩统一表意文字扩展A CJK Unified Ideographs Extension A
4DC0-4DFF   易经六十四卦符号    Yijing Hexagrams Symbols
4E00-9FFF   中日韩统一表意文字  CJK Unified Ideographs
F900-FAFF   中日韩兼容表意文字  CJK Compatibility Ideographs
FE00-FE0F   异体字选择符    Variation Selector
FE20-FE2F   组合用半符号    Combining Half Marks
FE30-FE4F   中日韩兼容形式  CJK Compatibility Forms
FF00-FFEF	半角及全角	Halfwidth and Fullwidth Forms
FFF0-FFFF	特殊	Specials
"""

# 每个计费的分割符 ，sep_range的子集
pay_range = """
2E80-2EFF   中日韩部首补充  CJK Radicals Supplement
31C0-31EF   中日韩笔画  CJK Strokes
3200-32FF   带圈中日韩字母和月份    Enclosed CJK Letters and Months
3300-33FF   中日韩兼容  CJK Compatibility
3400-4DBF   中日韩统一表意文字扩展A CJK Unified Ideographs Extension A
4E00-9FFF   中日韩统一表意文字  CJK Unified Ideographs
F900-FAFF   中日韩兼容表意文字  CJK Compatibility Ideographs
FE30-FE4F   中日韩兼容形式  CJK Compatibility Forms
"""

# 其他词都合并成词


regex = None

def _get_tuple_list(s):
    """
    预处理正则（匹配两个range的unicode序号段）
    """
    return [(m.group('begin'), m.group('end')) for m in
            re.finditer(r'(?P<begin>[0-9A-Fa-f]{4})-(?P<end>[0-9A-Fa-f]{4})', s)]  # 匹配两个range的unicode序号段


def _get_range(s):
    """
    预处理正则 （组装正则字符串）
    """
    join1 = u''.join(ur"%s-%s" % (unichr(int(b, 16)), unichr(int(e, 16))) for b, e in _get_tuple_list(s))
    return join1


def init_ranges():
    """
    预处理正则 （组装正则pattern）
    """
    global regex
    # 中日韩
    all = ur'[%(pay_range)s]|[^%(sep_range)s]+'\
          % {
        'pay_range': _get_range(pay_range),
        'sep_range': _get_range(sep_range)
    }  # 单独成词 | 组合成词+
    # print 'all', all
    regex = re.compile(all)


def _word_cnt(content):
    """
    返回所有计费单元的迭代器
    """
    global regex
    if not regex:
        init_ranges()
    return re.finditer(regex, content)


def word_cnt(content):
    # 使用sum因为re.finditer返回的是iterator不是数组，用sum不用存储所有元素，降低此步骤空间复杂度
    return sum(1 for _ in _word_cnt(content))


def test_word_cnt():
#    for i, w in enumerate(_word_cnt(u"£2ༀ3֐2ɐ⁰aa,df,d。ifsfs⑀df,fssod")):
#        print i, ',', w.group(0), 'len'#, len(w)
#    assert word_cnt(u"£2ༀ3֐2ɐ⁰aa,df,d。ifsfs⑀df,fssod") == 2
    for i, w in enumerate(_word_cnt(u'By installing the application you agree to')):
        print i, ',', w.group(0), 'len'#, len(w)
    print "word_cnt", word_cnt(u'By\xa0installing\xa0the\xa0application\xa0you\xa0agree\xa0to')
#    assert word_cnt(u'我们，是。 按时 asdfoijoij') == 6
#    print _word_cnt(u'We will, we will,rock you.')
##    assert word_cnt(u'We will, we will,rock you.') == 5
#    for i, w in enumerate(_word_cnt(u"""
#    曾宝仪关心
#　　虽已正式进入司法程序，但外传曾志伟将面对的刑罚较可能是普通殴打罪，若是初犯，最后以罚钱收场的机率极高。但若真的被控刑
#    事恐吓罪，最高可监禁5年。他女儿曾宝仪(阿宝)昨透过经abdsafd纪公司表示：“已经发短信关心爸爸了，但还没有得到回复。如果真的严重
#    的话，爸爸会主动告知的。”
#    """)):
#        print i, w.group(0)


if __name__ == '__main__':
#    import time
#    t = time.time()
#    for i in range(1000000):
#     test_word_cnt()
    for i, w in enumerate(_word_cnt(u"Deer's Ta-i_l")):
        print w.group(0)
        # print 'No.%i: %d' % (i, w.group(0))
#    print time.time() -t