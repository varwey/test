# -*- coding: utf-8 -*-
import re
__author__ = 'Zou'

__all__ = ['get_translate_content']

reg_str = "\[{3}[^\[\]]*\]{3}"


class RegReplace(object):
    def __init__(self, content):
        self.content = content

    def replace_string(self, mat_obj):
        if mat_obj:
            start_tig = mat_obj.start()
            end_tig = mat_obj.end()
            if self.content[start_tig-1] != '[' and self.content[end_tig] != ']':
                replace_str = ''
            else:
                replace_str = mat_obj.group(0)
            return replace_str


def get_translate_content(orig_content):
    reg_obj = re.compile(reg_str)
    regReplace = RegReplace(orig_content)
    return re.sub(reg_obj, regReplace.replace_string, regReplace.content)


if __name__ == '__main__':
    content = u'''
微博网友 @函[馆在]网上[[爆出]]一[[[张疑]]]似日[[[[本运营]]]]商的宣传海报。据海报显示，下一代的 iPhone 5S 将于 6 月 20 日发布，可于 7 月接收预定。iPhone 5S 将增加指纹识别功能，摄像头由现有的[[[ 800W提升到1300W]]]，并且 iOS 7的UI 界面将有较大
'''
    print get_translate_content(content)