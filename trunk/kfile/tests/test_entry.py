# #coding=utf8
#
# import time
# from kfile.controls.entry import get_entry_class
# from kfile.controls.session import file_sessionCM
#
#
#
# def test_insert_entries():
#     words_list = []
#     for i in range(6):
#         words_list.append(("%saaaa" %i))
#     positions = [1,5,3,2,4]
#     words_list = [("hello", 5), ("test", 3), ("world", 7), ("world2", 6)]
#     file_id = 5987119101086007317
#     with file_sessionCM("entry") as session:
#         Entry = get_entry_class(file_id)
#         Entry.create_multi(words_list, file_id, 123)
#
# def test_del_entries():
#     file_id = 5987119101086007317
#     with file_sessionCM("entry") as session:
#         Entry = get_entry_class(file_id)
#         print Entry.del_multi(file_id)
#
# def calculate_words(s, encoding='utf-8'):
#     import re
#     from types import StringType
#
#     # RX = re.compile(u"[a-zA-Z0-9_\u0392-\u03c9]+|[\u4E00-\u9FFF\u3400-\u4dbf\uf900-\ufaff\u3040-\u309f\uac00-\ud7af]+", re.UNICODE)
#     RX = re.compile(u"[a-zA-Z0-9_\u0392-\u03c9]+|[\u4E00-\u9FFF]+", re.UNICODE)
#
#     if type(s) is StringType:
#         s = unicode(s, encoding, 'ignore')
#
#     splitted = RX.findall(s)
#
#     CJK_count = 0
#     ASC_count = 0
#
#     for word in splitted:
#         if ord(word[0]) >= 12352:   # \u3040
#             CJK_count += len(word)
#             print word
#         else:
#             ASC_count += len(word)
#
#     return CJK_count, ASC_count
def test():
    ttt = 0
    global ttt, aaa
    ttt = 1
    aaa = 2
    print ttt

if __name__ == "__main__":
    test()
    print ttt
    # t1 = time.time()
    # # for i in range(1000000):
    # #     file_id = 5987119101086007318 + i
    # #     # t2 = time.time()
    # #     temp = file_id % 100
    # # t3 = time.time()
    # # print t3-t1
    # test_insert_entries()
    # t2 = time.time()
    # # test_del_entries()
    # # t3 = time.time()
    # print t2 - t1
    # print t3 - t2
    # test_str = "平假名 12352-12447 test hello こんにちは 안녕하세요 日文字母的草体,,"
    # print len(test_str)
    # print calculate_words(test_str)


