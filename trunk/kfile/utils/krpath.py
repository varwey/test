'''
Created on 2012-2-9

@author: admin
'''
import posixpath

def get_ext(path):
    ret = posixpath.splitext(path)[1][1:]
    if ret:
        return ret
    return posixpath.basename(path).partition('.')[2]


if __name__ == "__main__":
    print get_ext("mltest/cn/www.baidu.com")
    print get_ext("mltest/cn/www.baidu.com/")
    print get_ext("mltest/cn/www.baidu.com/file")
    print get_ext("mltest/cn/www.baidu.com/path/to/file.ext")