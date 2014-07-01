# -*- coding: utf-8 -*-
from Libs.self_trans.trans_cntw.word_utils import need_translation
from Libs.strs.opencc_wrapper import opencc


def try_to_translate(origin, src_lang, tar_lang):
    """
    尝试迅速翻译。如果返回None，尝试迅速翻译, 否则为成功。
    """
    if not need_translation(origin):
        return origin
    if src_lang == 'cn' and tar_lang == 'tw':
        if isinstance(origin, unicode): origin = origin.encode('utf8')
        return opencc('s2t', origin)
    elif src_lang == 'tw' and tar_lang == 'cn':
        if isinstance(origin, unicode): origin = origin.encode('utf8')
        return opencc('t2s', origin)


separator = "$$xc$$"
def merge_word_list(origin_list, src_lang, tar_lang):
    """
    把多个词条合并后用opencc翻译，再拆为原来的数组。
    """
    temp = separator.join(origin_list)
    temp = try_to_translate(temp, src_lang, tar_lang)
    
    if isinstance(temp, unicode):
        temp = temp.encode('utf8')
    destination = temp.split(separator)
    return destination


if __name__ == '__main__':
    print try_to_translate("我们是祖国美丽的花朵，乾隆干净软体", 'cn', 'tw')
    print try_to_translate("我們是祖國美麗的花朵，乾隆乾淨軟體", 'tw', 'cn')
    
    test_list1 = merge_word_list(["我们是祖国美丽的花朵", "乾隆干净软体", "蜡笔小新"], 'cn', 'tw')
    test_list2 =  merge_word_list(["我們是祖國美麗的花朵", "乾隆乾淨軟體", "蠟筆小新"], 'tw', 'cn')
    print "test_list1:"
    for word in test_list1:
        print word
    print "test_list2:"
    for word in test_list2:
        print word