# -*- coding: utf-8 -*-
import StringIO
from contextlib import closing
import xlrd, xlwt
from xlrd import XL_CELL_TEXT
from xlutils.copy import copy as xlutils_copy
from kfile.utils.kfile_logging import logger
from Libs.strs.coding_util import get_unicode


def extract(file_content):
    rb = xlrd.open_workbook(file_contents=file_content)
    word_list = []

    for rs in rb.sheets():
        logger.debug("Sheet: %s"%rs.name)
        for row in range(rs.nrows):
            for col in range(rs.ncols):
                c = rs.cell(row, col)
                if c.ctype == XL_CELL_TEXT:
                    word = c.value
                    if word and word.strip():
                        word_list.append(get_unicode(word.strip()))

    return word_list


def integrate(file_content, entry_list):
    """
        :param entry_list: a list store relation of src_words and their translate result, such as [(src1, trans1),(src2, trans2)]
    """
    words_dict = {}
    for entry in entry_list:
        words_dict[entry[0]] = entry[1]

    rb = xlrd.open_workbook(file_contents=file_content)
    wb = xlutils_copy(rb)
    i = 0
    for num, rs in enumerate(rb.sheets()):
        ws = wb.get_sheet(num)
        for row in range(rs.nrows):
            for col in range(rs.ncols):
                c = rs.cell(row, col)
                if c.ctype == XL_CELL_TEXT:
                    word_strip = c.value.strip()
                    try:
                        if word_strip and i < len(entry_list) and entry_list[i][1] is not None:
                            if word_strip == entry_list[i][0]:
                                ws.write(row, col, entry_list[i][1])
                                i += 1
                            else:
                                if words_dict.get(word_strip, None) is not None:
                                    ws.write(row, col, words_dict.get(word_strip, None))
                                    i += 1
                    except Exception, e:
                        logger.error("xls translate error in the integrate, lack translate result of entry(%s)" % word_strip)
                        raise Exception(e)
                    # if word_strip in word_dict and word_dict[word_strip]:
                    #     ws.write(row, col, word_dict[word_strip])

    with closing(StringIO.StringIO()) as sio:
        wb.save(sio)
        sio.seek(0)
        return sio.read()


if __name__ == '__main__':
    import os
    from kfile.utils.fileUtil import read_file, write_file
    import sys
    print sys.getdefaultencoding()
    # dirname = "E:\\xls"
    # excel_file_path = os.path.join(dirname, "AOE-活动库.xls").decode("utf8").encode("gbk")
    excel_file_path = "/root/share/nee2.xls"
    print type(excel_file_path)
    print os.path.exists(excel_file_path)
    content = read_file(excel_file_path)

    print len(content)

    word_list = extract(content)
    i = 0

    word_list2 = extract(content)
    # for i in range(len(word_list)):
    #     if word_list[i] != word_list2[i]:
    #         print "aaaaaaaaaaaaaaaaaaaaaaa", word_list[i], word_list2[i]
    #     if i <20 :
    #         print "*******", word_list[i]
    # print "ddddddddaaaaaaa", len(word_list)

    outfile = "/root/share/bbbbb.txt"
    test = open(outfile, "rw")
    for word in word_list:
        test.write(word)
    test.save()




    # word_dict = dict()
    # for word in word_list:
    #     word_dict[word] = word + "translated"
    #
    # print type(content)
    w_content = integrate(content, word_list)
    # # print len(w_content)
    # # write_file(w_content, os.path.join(dirname, "result.xls"))

    # wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)  ##第二参数用于确认同一个cell单元是否可以重设值。
    #
    # sheet.write(0,0,'some text')
    # sheet.write(0,0,'this should overwrite')   ##重新设置，需要cell_overwrite_ok=True
    #
    # style = xlwt.XFStyle()
    # font = xlwt.Font()
    # font.name = 'Times New Roman'
    # font.bold = True
    # style.font = font
    # sheet.write(0, 1, 'some bold Times text', style)
    #
    # wbk.save("/root/share/07excel.xlsx")    ##该文件名必须存在
