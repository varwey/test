# coding=utf-8
import re

__author__ = 'Jared'

variable_list = [
    r'\${[a-zA-Z0-9]+?}', # e.g ${user}
    r'%[_a-zA-Z][_a-zA-Z0-9]*?%', # e.g %user%
    r'%[0-9]?\.?[0-9]*[a-zA-Z]', # e.g %5.d
    r'{\s*?[_a-zA-Z0-9]*?}', # e.g {user}, {1}
    r'\\n', # Prevent \n => \ n
    r'\n', # Prevent \n => \ n
    r'&lt;', # Prevent &lt; => <
    r'&quot;', # Prevent &quot; => "
    r'&gt;', # Prevent &gt; => >
    r'&apos;', #Prevent &apos; => "
]

excape_pat = re.compile(r"&#(?P<uni>[0-9]{2,4});|(?P<na>&[a-zA-Z]{2,4};)")

excapes = {
"&ensp;":unichr(8194),
"&emsp;":unichr(8195),
"&nbsp;":unichr(160),
"&lt;":unichr(60),
"&gt;":unichr(62),
"&amp;":unichr(38),
"&quot;":unichr(34),
"&copy;":unichr(169),
"&reg;":unichr(174),
"&times;":unichr(215),
"&divide;":unichr(247),
}

class GoogleWordHelper(object):
    """
    处理谷歌翻译的变量问题
    谷歌翻译会使变量弄坏， 在此把所有不希望谷歌翻译的字符全部替换成为一个特定的字符串， 翻译完后再替换回去。
    Assumption: String like xxx0xxxx would not be changed during translation.
    """
    def __init__(self, origin):
        self.origin = origin
        self._i = 0
        replace_list = []
        def _rep(m):
            ret = 'xxx%dxxxx' % self._i
            self._i += 1
            replace_list.append((ret, m.group(0)))
            return " " + ret +" "

        self.replace_list = replace_list

        #: e.g I have %d apple  ==> I have xxx0xxxx apple.
        _tp = origin
        for pat in variable_list:
            _tp = re.subn(pat, _rep, _tp, flags=re.IGNORECASE)[0]
        self.variable_free_origin = _tp

    def recover_variable(self, translation_result):
        for k, v in self.replace_list:
            translation_result = re.subn(k, lambda s: v, translation_result, count=1, flags=re.IGNORECASE)[0]
#        for k, v in self.replace_list:
#            k = re.compile(re.escape(k), re.IGNORECASE)
#            translation_result = re.sub(k, v, translation_result)
        return self.clean(translation_result)

    def clean(self, tar):
        """
        去掉多余的转义
        :return:
        """
        m = re.search(excape_pat, tar)
        if not m: return tar # 没有转义字符
        if re.search(excape_pat, self.origin): return tar# 原串也有转移字符
        def _repl(m):
            uni = m.group('uni')
            na = m.group('na')
            return excapes.get(na, na) if na else unichr(int(uni))
        return re.subn(excape_pat, _repl, tar)[0]




def test():
    print GoogleWordHelper('"%s" has exist in panel %d! You can use the Add button to add in any panel').variable_free_origin
    print GoogleWordHelper('"%s" has exist in panel %d! You can use the Add button to add in any panel').recover_variable("&quot;Xxx0xxxx&quot; has exist in panel %d! You can use the Add button to add in any panel")
    print GoogleWordHelper("Location of advertisement resource can't be empty").recover_variable("Location of advertisement resource can&#39;t be empty")
    print GoogleWordHelper("Location of advertisement resource can't be empty").recover_variable("Location of advertisement resource can&quot;t be empty")




if __name__ == '__main__':
    test()