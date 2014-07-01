# -*- coding: utf-8 -*-

# __author__ = "hhl"

from kfile.translation.file.docx.translate import DocxParseHandler
from kfile.translation.file.word_handler import WordHandler
import string
import random

def gen_random_name():
    return string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l'], 12)).replace(" ", "")

class DocxWordHandler(WordHandler):
    ext = "docx"
    def __init__(self):
        self.parse_handler = DocxParseHandler()

    def extract(self, content, user_upload=False):
        """
        extract words from pptx file, and return a words list
        """

        return self.parse_handler.extract(file_contents=content)

    def integrate(self, content, word_list, user_upload=False):
        """
        content：文件内容；
        word_list：原词与翻译结果的对应关系, such as [("src_word1": "trans_word1"), ("src_word2": "trans_word2")]。
        该方法将翻译结果回填到文件。返回翻译好的文件内容
        """
        entry_list = []
        for word in word_list:
            entry_list.append(word[1])
        return self.parse_handler.integrate(src_content= content, entry_list=entry_list)


if __name__ == "__main__":
    import pprint
    # word_dict = {"fine": "xingcloud", "xingcloud": "YBN", "sheji":"design","SEQ Figure \\* ARABIC":"1", "Hello how are you":u"终于好了", " image 1":" Photo 1"}
    # word_list = [None, None, u"{0}It{1}’{2}s{3} ok{4}, Nice {5}thaole et {6}you~", u"{0}每一件事情 {1}jiang{2} ok!", None, None,
    #                  u"{0}aaaaaaaaaaaaaaaa",None, None
    #              ]

    word_list = [
            u"{0}test介绍：",
            u"{0}作为{1}NoSQL{2}的一个重要类型，文档型{3}NoSQL{4}通常被认为是最接近传统关系型数据库的{5}NoSQL{6}。文档型{7}NoSQL{8}的核心是数据嵌套，这种设计可以从某{9} {10}种程度上大大简化传统数据库复杂的关联问题。同时由于摆脱了关系模型里面的强一致性限制，文",
            u"{0}档型{1}NoSQL{2}还可以做到水平扩张与高可用。相比其他的{3} {4}NoSQL{5}类型，文档型{6}NoSQL{7}的应用范围要广泛的多。",
            u"",
            u"{0}常见的文档型{1}NoSQL{2}包括{3}shujuku{4}、{5}CouchDB{6}等，其中{7}database{8}是一个高性能、开源、{9}无模式{10}的文档型数据库，它在许多场景下可用于替代传统的关系型数据库或键{11}/{12}值存储方式。{13}SequoiaDB{14}（巨杉数据库）作为文档型{15}NoSQL{16}家族中的新成员，其企",
            u"{0}业级的{1}新特性颇受关注。该数据库在提供文档类{2}JSON{3}接口的同时，能够替代{4}HBase{5}作为{6}Hadoop{7}的存储引擎。与{8}MongoDB{9}相比，其{10}Hadoop{11}接口较为完善。",
            u"",
            u"{0}测试全文：{1}NoSQL{2}性能测试：{3}MongoDB{4} VS.{5} {6}SequoiaDB",
            u"",
            u"{0}hello how are you.{1}下载地址：",
            u"{0}Sequoiadb-1.3 for IBM Power Linux 64 Installer 202.60MB",
            u"{0}test list-1.3 for Linux x86_64 Installer 201.72MB",
            u"{0}SequoiaDB{1} Demo VMware {2}虚机镜像{3}（只能体验功能，不能测试性能和{4}可{5}扩展性）",
            u"{0}SequoiaDB{1}教程：{2}SequoiaDB{3}信息中心",
            u"",
            u"{0}活动fine：",
            u"{0}1{1}、阅读测试报告，提出您的观点以及您在{2}NoSQL{3}中可能需要测试的场景",
            u"{0}2{1}、下载虚拟机，体验功能；或者下载和部署社区版，测试性能和{2}可{3}扩展性",
            u"{0}3{1}、在您的测试环境中部署{2}SequoiaDB{3}社区版，测试性能并提交测试报告（参考本篇测试报告）",
            u"",
            u"{0}活动时间：{1}10{2}月{3}gggga{4}日{5}-10{6}月{7}30{8}日",
            u"",
            u"{0}活动ok?：",
            u"{0}1{1}、提出重要功能建议或撰写优秀测试报告的前{2}3{3}名用户，奖励价值一千元的{4}Kindle {5}Paperwhite{6}电子书阅读器一部，共{7}3{8}部",
            u"{0}2{1}、所有阅读报告，并下载测试的用户，均有机会获得{2}geek{3}范{4}十足的{5}SequoiaDB{6} {7}帽衫{8}一件！共{9}10{10}件",
            u"",
            u"{0}报告提交：",
            u"{0}1{1}、{2}参与跟帖{3}，将测试报告的相关内容发布出来",
            u"{0}2{1}、邮件到{2} {3}rmzhou{4} (AT) staff.chinaunix.net{5}，在征得您的同意下，将相关内容公布到这个帖子中来"
        ]
    src_file = "/media/sf_D_DRIVE/ttt.docx"
    tar_file = "/media/sf_D_DRIVE/testdoc2.docx"
    doc_handle = DocxWordHandler()
    list = doc_handle.extract(src_file)
    # print "["
    # for word in list:
    #     print "u\"%s\"," % word
    # print "]"
    print len(list)
    # pprint.pprint(list)
    doc_handle.integrate(src_file, tar_file, word_list)
    # print doc_handle.extract(tar_file)
    # temp_str = u'{0}Test 1{1}; test2.'
    # print get_seqRun_content_rel(temp_str)