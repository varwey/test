#!-*- coding:utf8 -*-
# import kfile
# kfile.initiate()
from Libs.strs.coding_util import str2utf8
from Libs.strs.word_cnt import word_cnt

from kfile.api import KFILE
kf = KFILE()

#创建源文件
# path = '/home/johnny/work/kfs/trunk/kf/tests/cn-《GS+Online》视频征集.txt'
path = '/root/t1.txt'
f = open(path)
path = 'xxxxxxxxxxxxxxxxx' + path
t_file = kf.create_orig_file('yyyy', path, 'cn', f.read())


file_id = t_file.id
print file_id
#
#
# 创建子文件
kf.create_compl_files(file_id, tar_langs=['us', 'jp', 'en'])
#

# 分解词条
print kf.extract(file_id)

#
#获取词条
src_words = kf.get_word_list('yyyy', file_id)
src_word_list = [word.word for word in src_words]
src_words_pos = [(word.word, word.position) for word in src_words]
print "len src word =", len(src_words)
#
import requests
import ujson
#
data = {
    'group_name':'yyyy',
    'sl': 'en',
    'tl': 'cn',
    'q': src_word_list,
}
#
# req = requests.post(
#     url="http://162.243.23.94/api/v1/translate",
#     data=data,
# )
#
# tar_dict = ujson.loads(req.text)['result']
# # print tar_dict
# #
# word_list = []
# for src_word, position in src_words_pos:
#     word_list.append((tar_dict.get(src_word, src_word), position))
# #
# # word_list = [item for item in word_list if item[1] % 2]
# print "len word_list = ", len(word_list)
# for i in word_list:
#     print i
# #
# #回写翻译结果
# print kf.fill_word_list(file_id, 'en', word_list, is_cover=True)

# #
# # # # 文件合成
# kf.integrate(file_id, 'en')
#
#
# # # # 获取内容
file =  kf.get_file(file_id, 'cn')
print file.content
# #
# #
# file =  kf.get_file(file_id, 'en')
# print file.content
#


# 获取内容
# files = kf.get_files('yyyy', 'cn', order='+path', page=1, size=2)
# for file in files:
#     print file.path


# # 获取词条
# entries = kf.get_entries('yyyy', 'cn', order='-position', page=1, size=7)
# for entry in entries:
#     print entry.word



# 删除文件
# print kf.delete(file_id)

test = "删除文件"
print word_cnt(str2utf8(test)[0])
