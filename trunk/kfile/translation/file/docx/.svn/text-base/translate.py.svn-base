# -*- coding: utf-8 -*-

# __author__ = "hhl"

from Libs.strs.coding_util import get_unicode
from lxml import etree
try:
    from PIL import Image
except ImportError:
    import Image
import zipfile
import tempfile
import os

from kfile.utils.translate.trans_seq_file import gen_random_name,  EntryListException, content_to_stringIO

nsprefixes = {
    'mo': 'http://schemas.microsoft.com/office/mac/office/2008/main',
    'o':  'urn:schemas-microsoft-com:office:office',
    've': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    # Text Content
    'w':   'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w10': 'urn:schemas-microsoft-com:office:word',
    'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
    # Drawing
    'a':   'http://schemas.openxmlformats.org/drawingml/2006/main',
    'm':   'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'mv':  'urn:schemas-microsoft-com:mac:vml',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'v':   'urn:schemas-microsoft-com:vml',
    'wp':  ('http://schemas.openxmlformats.org/drawingml/2006/wordprocessing'
            'Drawing'),
    # Properties (core and extended)
    'cp':  ('http://schemas.openxmlformats.org/package/2006/metadata/core-pr'
            'operties'),
    'dc':  'http://purl.org/dc/elements/1.1/',
    'ep':  ('http://schemas.openxmlformats.org/officeDocument/2006/extended-'
            'properties'),
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    # Content Types
    'ct':  'http://schemas.openxmlformats.org/package/2006/content-types',
    # Package Relationships
    'r':  ('http://schemas.openxmlformats.org/officeDocument/2006/relationsh'
           'ips'),
    'pr':  'http://schemas.openxmlformats.org/package/2006/relationships',
    # Dublin Core document properties
    'dcmitype': 'http://purl.org/dc/dcmitype/',
    'dcterms':  'http://purl.org/dc/terms/'}


class DocxParseHandler():
    def __init__(self):
        pass

    def opendocx(self, file):
        '''Open a docx file, return a document XML tree'''
        mydoc = zipfile.ZipFile(file)
        try:
            xmlcontent = mydoc.read('word/document.xml')
            document = etree.fromstring(xmlcontent)
        except Exception, e:
            raise Exception(e)
        finally:
            mydoc.close()
        return document

    def extract(self, file_path= None, file_contents=None ):
        """
        extract words from pptx file, and return a words list
        """
        file = content_to_stringIO(file_path, file_contents)

        document = self.opendocx(file)

        entry_list = []
        # Compile a list of all paragraph (p) elements
        paralist = []
        serial_para = 0
        for element in document.iter():
            # Find p (paragraph) elements
            if element.tag == '{'+nsprefixes['w']+'}p':
                paralist.append(element)
        # Since a single sentence might be spread over multiple text elements,
        # iterate through each paragraph, appending all text (t) children to that
        # paragraphs text.
        for para in paralist:
            src_paratext = u''
            # Loop through each paragraph
            for element in para.iter():
                # Find t (text) elements
                if element.tag == '{'+nsprefixes['w']+'}t':
                    if element.text:
                        src_paratext = src_paratext + element.text
                        # print serial_run, paratext
                # elif element.tag == '{'+nsprefixes['w']+'}tab':
                #     paratext = paratext + '\t'

            # Add our completed paragraph text to the list of paragraph text
            if len(src_paratext.strip()):
                entry_list.append(get_unicode(src_paratext))
                serial_para += 1
        return entry_list

    def integrate(self, src_file=None, src_content=None, tar_file=None, entry_list= None):
        """
        :param src_file:  source pptx file
        :param tar_file:  tar file after translating
        :param entry_list: the dict stores the results of translate words
        :return: if success ,return true
        """
        file = content_to_stringIO(src_file, src_content)
        mydoc = zipfile.ZipFile(file)
        try:
            xmlcontent = mydoc.read('word/document.xml')
            document = etree.fromstring(xmlcontent)
            print "len=", len(entry_list)
            paralist = []
            serial_para = 0
            num_para = 0
            null_para = []
            i = 0
            for element in document.iter():
                # Find p (paragraph) elements
                if element.tag == '{'+nsprefixes['w']+'}p':
                    paralist.append(element)

            for para in paralist:
                src_paratext = u''
                # Loop through each paragraph
                for element in para.iter():
                    # Find t (text) elements
                    if element.tag == '{'+nsprefixes['w']+'}t':
                        if element.text:
                            src_paratext = src_paratext + element.text

                # Add our completed paragraph text to the list of paragraph text
                if len(src_paratext.strip())>0:
                    num_para += 1
                else:
                    null_para.append(i)
                i += 1

            len_entry_list = len(entry_list)
            if len_entry_list != num_para:
                info = u"The entry_list (%s) missed some paragraphs!" % entry_list
                raise EntryListException(info)

            i = 0
            for para in paralist: # Loop through each paragraph
                paratext = u''

                if i in null_para:
                    i += 1
                    continue
                i += 1
                if entry_list[serial_para] is None:
                    serial_para +=1
                    continue

                flag = 0
                for element in para.iter():
                    # Find t (text) elements
                    if element.tag == '{'+nsprefixes['w']+'}t':
                        if element.text:
                            if flag:
                                element.text = u''
                            else:
                                flag = 1
                                element.text = entry_list[serial_para]

                serial_para += 1

            file_list = mydoc.namelist()
            treesandfiles = {}
            for f in file_list:
                if f == "word/document.xml":
                    treesandfiles[f] = document
                    continue

                treestring = mydoc.read(f)
                treesandfiles[f] = treestring

            need_del = 0
            if tar_file is None:
                if src_file is not None:
                    tar_file = src_file
                else:
                    temp_dir = tempfile.mkdtemp()
                    need_del = 1
                    tar_file = "%s/%s.docx" % (temp_dir, gen_random_name())

            tar_doc = zipfile.ZipFile(tar_file, mode='w', compression=zipfile.ZIP_DEFLATED)
            try:
                for file_path in treesandfiles:
                    if file_path == "word/document.xml":
                        treestring = etree.tostring(treesandfiles[file_path], pretty_print=True)
                    else:
                        treestring = treesandfiles[file_path]
                    tar_doc.writestr(file_path, treestring)
            except Exception, e:
                raise EntryListException(e)
            finally:
                tar_doc.close()

        except Exception, e:
            raise EntryListException(info)
        finally:
            mydoc.close()

        with open(tar_file, "r") as fp:
            content = fp.read()
            fp.close()

        if need_del:
            if os.path.exists(tar_file):
                os.remove(tar_file)
                os.rmdir(temp_dir)

        return content

if __name__ == "__main__":
    import pprint
    # word_dict = {"fine": "xingcloud", "xingcloud": "YBN", "sheji":"design","SEQ Figure \\* ARABIC":"1", "Hello how are you":u"终于好了", " image 1":" Photo 1"}
    # word_list = [None, None, u"{0}It{1}’{2}s{3} ok{4}, Nice {5}thaole et {6}you~", u"{0}每一件事情 {1}jiang{2} ok!", None, None,
    #                  u"{0}aaaaaaaaaaaaaaaa",None, None
    #              ]

    word_list = [
u"背景dddddddddddddddddddd介绍：",
u"“作为NoSQL的一个重要dddddddddddddddd类型，文档型NoSQL通常被认为是最接近传统关系型数据库的NoSQL。文档型NoSQL的核心是数据嵌套，这种设计可以从某 种程度上大大简化传统数据库复杂的关联问题。同时由于摆脱了关系模型里面的强一致性限制，文”",
u"档型NoSQL还可以做”到”水平扩张与高可用。相比其他的 NoSQL类型，文档型NoSQL的应用范围要广泛的多。",
u"常见的文档型NoSQL包括MongoDB、CouchDB等，其中MongoDB是一个高性能、开源、无模式的文档型数据库，它在许多场景下可用于替代传统的关系型数据库或键/值存储方式。SequoiaDB（巨杉数据库）作为文档型NoSQL家族中的新成员，其企",
u"业级的新特性颇受关注。该数据库在提供文档类JSON接口的同时，能够替代HBase作为Hadoop的存储引擎。与MongoDB相比，其Hadoop接口较为完善。",
u"测试全文：NoSQL性能测试：MongoDB VS. SequoiaDB",
u"SequoiaDB下载地址：",
u"Shehelkajdflkjflsdkfjldskfjlkjflstaller 202.60MB",
u"Seqhaole Installer 201.72MB",
u"SequoiaDB Demo VMware 虚机镜像（只能体验功能，不能测试性能和可扩展性）",
u"SequoiaDB教程：SequoiaDB信息中心",
u"活动参与：",
u"1、阅读测试报告，提出您的观点以及您在NoSQL中可能需要测试的场景",
u"2、下载虚拟机，体验功能；或者下载和部署社区版，测试性能和可扩展性",
u"3、在您的测试环境中部署SequoiaDB社区版，测试性能并提交测试报告（参考本篇测试报告）",
u"活动时间：10月1日-10月30日",
u"活动奖励：",
u"1、提出重要功能建议或撰写优秀测试报告的前3名用户，奖励价值一千元的Kindle Paperwhite电子书阅读器一部，共3部",
u"2、所有阅读报告，并下载测试的用户，均有机会获得geek范十足的SequoiaDB 帽衫一件！共10件",
u"报告提交：",
u"1、参与跟帖，将测试报告的相关内容发布出来",
u"2、邮件到 rmzhou (AT) staff.chinaunix.net，在征得您的同意下，将相关内容公布到这个帖子中来",
]
    src_file = "/media/sf_D_DRIVE/ttt.docx"
    tar_file = "/media/sf_D_DRIVE/testdoc2.docx"
    doc_handle = DocxParseHandler()

    fp = open(src_file, "r")
    file_contents = fp.read()
    list = doc_handle.extract(file_contents=file_contents)
    print "["
    for word in list:
        print "u\"%s\"," % word
    print "]"
    # pprint.pprint(list)
    doc_handle.integrate(src_file= src_file, tar_file=tar_file, entry_list=word_list)
    list = doc_handle.extract(file_path=tar_file)
    # print "["
    # for word in list:
    #     print "u\"%s\"," % word
    # print "]"
    # print len(list)
    # print doc_handle.extract(tar_file)
    # temp_str = u'{0}Test 1{1}; test2.'
    # print get_seqRun_content_rel(temp_str)
