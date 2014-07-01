# -*- coding: utf-8 -*-
import csv
from StringIO import StringIO
import sys
from Libs.strs.coding_util import get_unicode
from kfile.utils.translate.file_integrate import replace_or_origin

reload(sys)
sys.setdefaultencoding( "utf-8" )

def extract(file_content):
    word_list = []
    buf = StringIO(file_content)
    csv_reader = csv.reader(buf)
    for line in csv_reader:
        for word in line:
            if not word or not word.strip():
                continue
            word_list.append(get_unicode(word))
    return word_list


def integrate(file_content, entry_list):
    words_dict = {}
    for entry in entry_list:
        words_dict[entry[0]] = entry[1]

    read_buf = StringIO(file_content)
    write_buf = StringIO()
    csv_reader = csv.reader(read_buf)
    csv_writer = csv.writer(write_buf)
    write_line = []
    len_list = len(entry_list)
    i = 0
    for line in csv_reader:
        for word in line:
            word = get_unicode(word)
            tar_word, i = replace_or_origin(word, i, entry_list, words_dict)
            write_line.append(tar_word)
            # if word in word_dict:
            #     write_line.append(word_dict[word])
            # else:
            #     write_line.append(word)
        csv_writer.writerow(write_line)
        write_line = []
    translated_file_content = write_buf.getvalue()
    return translated_file_content


if __name__ == '__main__':
    fs = open('test.csv')
    file_content = fs.read()
    fs.close()
    extract(file_content)
    a = dict()
    a[u'6'] = u'six'
    a[u'line1'] = u'第一行'
    print integrate(file_content, a)