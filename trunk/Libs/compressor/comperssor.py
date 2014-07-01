# -*- coding=utf-8 -*-
import commands
import os
import tempfile
import re

__author__ = 'zou'


class JSCompilationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

def compressor_js(js_code):
    yuicompressor = "yuicompressor-2.4.7.jar"
    compressor_path = os.path.join(os.path.dirname(__file__), yuicompressor)

    with tempfile.NamedTemporaryFile(delete=False) as sf:
        sf.write(js_code)
        sf_path = sf.name

    cmd = "java -jar %(compressor_path)s --charset utf-8 --type js %(src_file)s" % dict(
        compressor_path=compressor_path,
        src_file=sf_path
    )
    compressed_code = commands.getoutput(cmd)
    pattern = re.compile("\[ERROR\]", re.I)
    if pattern.search(compressed_code):
        raise JSCompilationError(compressed_code)

    os.remove(sf_path)

    return compressed_code


if __name__ == "__main__":

    js_file = open("./test.js")
    print compressor_js(js_file.read())






