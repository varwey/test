# coding=utf-8
"""
    gzip压缩与解压缩
    author: liuxiong
"""
import gzip
import StringIO
from contextlib import closing

def gzip_compress(content):
#    out = StringIO.StringIO()
#    gzip.GzipFile(fileobj=out, mode="w").write(content)
#    out.flush()
#    data = out.getvalue()
#    out.close()
#    return data
    with closing(StringIO.StringIO()) as out:
        gzip.GzipFile(fileobj=out, mode="w").write(content)
        out.flush()
        return out.getvalue()


def gzip_decompress(data):
    return gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()


if __name__ == "__main__":
    with closing(open(__file__, 'r')) as file:
        data = gzip_compress(file.read())
        print data
        print "====================================================="
        content = gzip_decompress(data)
        print content
