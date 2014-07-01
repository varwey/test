"""
Created on 2012-1-19
@author: onfire
This class helps to generate the path of a hidden file from the original file and vice versa.
"""
import posixpath


def get_prefix(path):
    if posixpath.splitext(path)[1]:
        return posixpath.splitext(path)[0]
    return ""


class GenFileHelper(object):
    
    """
    Usage:
            tp = GenFileHelper(abspath, GAME_HIDDEN_DIRNAME)
            genXML = tp.get_hidden_path('.xml')
            genCSS = tp.get_hidden_path('.css')
    """

    def __init__(self, path, hidden_dirname):
        elements = path.split('?')
        if len(elements) > 1:
            self.params = '?' + elements[1]
        else:
            self.params = ''

        path = elements[0]

        self.hidden_dirname = hidden_dirname
        if posixpath.basename(posixpath.dirname(path)) == hidden_dirname:
            self.main_file_no_ext = get_prefix(
            posixpath.join(posixpath.dirname(posixpath.dirname(path)), posixpath.basename(path)))
        else:
            self.main_file_no_ext = get_prefix(path)


    def get_main_file(self, ext):
        if not ext.startswith('.'):
            ext = '.' + ext
        return self.main_file_no_ext + ext + self.params


    def get_hidden_path(self, ext):
        if not ext.startswith('.'):
            ext = '.' + ext
        ret = posixpath.join(posixpath.dirname(self.main_file_no_ext), self.hidden_dirname,
            posixpath.basename(self.main_file_no_ext) + ext)

        return ret + self.params


if __name__ == '__main__':
    helper = GenFileHelper('abc/dd/f.xml?k=v', '.xc_locale')
    print helper.get_hidden_path('.swf')
    print helper.get_main_file('.css')
    helper = GenFileHelper('.xml', '.xc_locale')
    print helper.get_hidden_path('.swf')
    helper = GenFileHelper('rr2.usxingcloud.com/6523079184_online/back/flash/main/xml/config.json?v=39.35144143179059',
                        '.xc_locale')
    print helper.get_hidden_path('css')
    print helper.get_hidden_path('.xml')