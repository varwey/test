# -*- coding: utf-8 -*-

# __author__ = "hhl"

import zipfile
import os
import tempfile
from lxml import etree
from Libs.strs.coding_util import get_unicode
from kfile.utils.translate.trans_seq_file import gen_random_name, EntryListException, content_to_stringIO

try:
    from PIL import Image
except ImportError:
    import Image

class PptxParseHandler():
    def __init__(self):
        pass

    def extract(self, file_path= None, file_contents=None ):
        """
        extract words from pptx file, and return a words list
        """
        file = content_to_stringIO(file_path, file_contents)
        word_list = []
        mydoc = zipfile.ZipFile(file)
        try:
            file_list = mydoc.namelist()
            slide_list = [f for f in file_list if f.startswith("ppt/slides/slide")]

            for slide in slide_list:
                xmlcontent = mydoc.read(slide)
                ppttree = etree.fromstring(xmlcontent)
                paralist = []
                for element in ppttree.iter():
                    # Find p (paragraph) elements
                    if element.prefix =='a' and element.tag.rsplit('}',1)[-1] == "p":
                        paralist.append(element)

                for para in paralist:
                    paratext = u''
                    src_paratext = u''
                    serial_run = 0
                    # Loop through each paragraph
                    for element in para.iter():
                        if element.text and element.prefix == 'a' and element.tag.rsplit('}',1)[-1] == "t":
                            src_paratext = src_paratext + element.text

                    if len(src_paratext.strip())>0:
                        word_list.append(get_unicode(src_paratext))
        except Exception,e :
            raise Exception(e)
        finally:
            mydoc.close()

        return word_list


    def integrate(self, src_file=None, src_content=None, tar_file=None, entry_list= None):
        """
        :param src_file:  source pptx file
        :param tar_file:  tar file after translating
        :param word_dict: the dict stores the results of translate words
        :return: if success ,return true
        """
        file = content_to_stringIO(src_file, src_content)

        mydoc = zipfile.ZipFile(file)
        try:
            file_list = mydoc.namelist()
            slide_list = [f for f in file_list if f.startswith("ppt/slides/slide")]

            ppt_trees= []
            paralist = []
            serial_para = 0
            num_para = 0
            null_para = []
            i = 0

            for slide in slide_list:
                xmlcontent = mydoc.read(slide)
                ppt_trees.append(etree.fromstring(xmlcontent))
                old_num_para = len(paralist)
                for element in ppt_trees[-1].iter():
                    # Find p (paragraph) elements
                    if element.prefix =='a' and element.tag.rsplit('}',1)[-1] == "p":
                        paralist.append(element)

                for k in range(old_num_para, len(paralist),1):
                    paratext = u''
                    src_paratext = u''
                    serial_run = 0
                    # Loop through each paragraph

                    for element in paralist[k].iter():
                        if element.text and element.prefix == 'a' and element.tag.rsplit('}',1)[-1] == "t":
                            src_paratext = src_paratext + element.text

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
                    if element.prefix == 'a' and element.tag.rsplit('}',1)[-1] == "t":
                        if element.text:
                            if flag:
                                element.text = u''
                            else:
                                flag = 1
                                element.text = entry_list[serial_para]

                serial_para += 1

            treesandfiles = {}
            j = 0
            for f in file_list:
                if f.startswith("ppt/slides/slide"):
                    treesandfiles[f] = ppt_trees[j]
                    j += 1
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
                    tar_file = "%s/%s.pptx" % (temp_dir, gen_random_name())
        except Exception, e:
            raise EntryListException(e)
        finally:
            mydoc.close()

        tar_doc = zipfile.ZipFile(tar_file, mode='w', compression=zipfile.ZIP_DEFLATED)
        try:
            for file_path in treesandfiles:
                if file_path.startswith("ppt/slides/slide"):
                    treestring = etree.tostring(treesandfiles[file_path], pretty_print=True)
                else:
                    treestring = treesandfiles[file_path]

                tar_doc.writestr(file_path, treestring)
        except Exception, e:
            raise EntryListException(e)
        finally:
            tar_doc.close()

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
    word_list = [u'Y yiwang',
 u'\u201c\u4f5c\u4e3aNoSddddddddddddddddddddddddddQL\u7684\u4e00\u4e2a\u91cd\u8981\u7c7b\u578b\uff0c\u6587\u6863\u578bNoSQL\u901a\u5e38\u88ab\u8ba4\u4e3a\u662f\u6700\u63a5\u8fd1\u4f20\u7edf\u5173\u7cfb\u578b\u6570\u636e\u5e93\u7684NoSQL\u3002\u6587\u6863\u578bNoSQL\u7684\u6838\u5fc3\u662f\u6570\u636e\u5d4c\u5957\uff0c\u8fd9\u79cd\u8bbe\u8ba1\u53ef\u4ee5\u4ece\u67d0 \u79cd\u7a0b\u5ea6\u4e0a\u5927\u5927\u7b80\u5316\u4f20\u7edf\u6570\u636e\u5e93\u590d\u6742\u7684\u5173\u8054\u95ee\u9898\u3002\u540c\u65f6\u7531\u4e8e\u6446\u8131\u4e86\u5173\u7cfb\u6a21\u578b\u91cc\u9762\u7684\u5f3a\u4e00\u81f4\u6027\u9650\u5236\uff0c\u6587\u201d',
 u'hello',
 u'world',
 u'welcome',
 u'You ',
 u'fine',
 u'\u8d3a\u6c47\u6797',
 u'Let\u2019s',
 u'go',
 u'Hehuilin',
 u'hello',
 u'world',
 u'welcome',
 u'You ',
 u'fine',
 u'\u8d3a\u6c47\u6797',
 u'Let\u2019s',
 u'go',
 u'hetestilin']

    pptx_handler = PptxParseHandler()
    src_path = "/media/sf_D_DRIVE/testppt.pptx"
    tar_path = "/media/sf_D_DRIVE/testppt2.pptx"
    result = pptx_handler.extract(src_path)
    pprint.pprint(result)
    print len(result)

    pptx_handler.integrate(src_file= src_path, tar_file=tar_path, entry_list=word_list)
    # print get_word_list(tar_path)