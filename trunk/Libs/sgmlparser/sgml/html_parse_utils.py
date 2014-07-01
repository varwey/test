#-*- coding=utf-8 -*-
import re
from Libs.sgmlparser.sgml.html_util import str2utf8


attrfindV2 = re.compile(
    r'\s*([a-zA-Z_][-:.a-zA-Z_0-9]*)(\s*=\s*'
    r'(\'[^\']*\'|"[^"]*"|[][\-a-zA-Z0-9./,:;+*%?!&$\(\)_#=~\'"@]*))?')
attrfind = re.compile(
    r'\s*([a-zA-Z_][-:.a-zA-Z_0-9]*)\s*=\s*'
    r'(\'[^\']*\'|"[^"]*")')

tag_find = re.compile(r'<([a-zA-Z_0-9]*)\s*')

class LineElement(object):
    def __init__(self, param_tuple):
        """param_tuple:('end_tag', (i, k), rawdata[i:k]) 即 (类型,位置,数据) 此时位置信息无用
        由sgmllibfix处理时候抛出的中间结果

        """
        self.param_tuple = param_tuple
        if not isinstance(self.param_tuple, tuple):
            pass

        """self.e_type ---> nomoretags,text,start_tag,end_tag,comment,doc_type """
        self.e_type = param_tuple[0]
        self.data = param_tuple[2]

        self.match_list = None

    @property
    def tag_name(self):
        """return tag name 闭合标签返回的是‘/tag_name’
        """
        if 'start_tag' == self.e_type:
            match = tag_find.match(self.data)
            if match:
                return match.group()[1:].strip().lower()
            else:
                return ''
        elif 'end_tag' == self.e_type:
            return self.data[1:-1].strip().lower()
        else:
            return ''
        pass

    @property
    def attr_dict(self):
        """return ｛ attr : attr_value ｝, A dict

        """
        if 'start_tag' == self.e_type:
            if not self.match_list: self.get_match_list()

            tmp = {m[1]: m[3] for m in self.match_list}
            for k, v in tmp.items():
                tmp[k] = v[1:-1]
                if tmp[k] == '':
                    del tmp[k]
                    continue
                tmp[k] = str2utf8(tmp[k])[0]
            return tmp

        else: return {}

    def has_attr(self, attr=None):
        """return true false,此片段实例是否包含属性信息

        """
        if 'start_tag' == self.e_type:
            match = attrfind.findall(self.data)
            if not match: return  False
            else:
                if attr in dict(match).keys():
                    return True
                else: return False
        else:
            return False

    def update_word(self, word):
        """replace text_node
        """
        if 'text' == self.e_type and len(self.data.strip()):
            self.data = word
            return self.data
        else:
            return False
        pass

    def update_attr(self, attr_key, target_attr_value):
        """replace attr
        """
        if not self.match_list: self.get_match_list()

        for m in self.match_list:
            if m[1] == attr_key: m[3] = '"%s"' % target_attr_value

        self.data = '%s%s' % (''.join([''.join(m) for m in self.match_list]), self.data_end)
        return self.data

    def update_data(self, data):
        """遗留方法:如，去掉自身、替换自身
        """
        self.data = data
        return self.data

    def get_match_list(self):
        self.match_list = []
        pre_i = 0
        for m in attrfind.finditer(self.data):
            m_list = []
            for i, j in m.regs[1:]:
                m_list.append(self.data[pre_i:i])
                m_list.append(self.data[i:j])
                pre_i = j

            self.match_list.append(m_list)

        self.data_end = self.data[pre_i:]


def gen2list(gen):
    """yield element to obj-list

    """
    return [item for item in gen if item is not None]


class stack(object):
    def __init__(self):
        self.stack = []

    def push(self, obj):
        return self.stack.append(obj)

    def pop(self):
        return self.stack.pop()

    def length(self):
        return len(self.stack)

    def empty(self):
        self.stack = []

    def top(self):
        if self.length():
            return self.stack[-1]
        else:
            return None

    def tolist(self):
        return self.stack


if __name__ == "__main__":
    src_data = '''<img title = "达到" version src  =   "http://image.ec21.com/周.jpg" border='0' xxx >'''
    p = LineElement(('start_tag', (2, 4), src_data))
    print p.attr_dict
    p.update_attr('title', 'HHH')
    p.update_attr('border', '100')

    print src_data
    print p.data

    src_data = '''<img >'''
    p = LineElement(('start_tag', (2, 4), src_data))
    print p.attr_dict
    p.update_attr('title', 'HHH')
    p.update_attr('border', '100')

    print src_data
    print p.data
