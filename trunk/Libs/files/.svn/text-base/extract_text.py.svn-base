# coding=utf8

"""
从各种文件中提取文本
支持的文件格式：
    http://tika.apache.org/1.3/formats.html
"""

import os
import tempfile
import traceback
from contextlib import closing
import subprocess


TIKA_JAR_PATH = os.path.join(os.path.dirname(__file__), 'tika-app-1.3.jar')


def extract_plain_text(file_content):
    with closing(tempfile.NamedTemporaryFile()) as temp_file:
        temp_file.write(file_content)
        temp_file.flush()

        try:
            output = subprocess.check_output(["java", "-jar", TIKA_JAR_PATH, "--text", "--encoding=utf8", temp_file.name])
        except subprocess.CalledProcessError:
            print traceback.format_exc()
            output = ""

        return output


if __name__ == "__main__":
    print TIKA_JAR_PATH
    pass