# coding=utf-8

import re
import StringIO
from lxml import etree
from lxml.etree import CDATA
from kfile.utils.kfile_logging import logger
from Libs.strs.coding_util import get_unicode
from kfile.translation.file.xml.xml_escape import unescape
from kfile.translation.file.xml.xpath import XMLSyntaxError, NoXPathInfoError
from kfile.translation.file.word_handler import WordHandler

ANDROID_NAMESPACES = 'http://schemas.android.com/apk/res/android'
ANDROID_XPATH_PATTERN_STRING = '//@android:textOn|//@android:textOff|//@android:text|//string/text()\
|//@android:description|//@android:label|//@android:hint|//@android:imeActionLabel|//@android:title\
|//@android:summary|//@android:dialogTitle|//@android:defaultValue|//@searchSettingsDescription\
|//@android:searchButtonText|//@android:voicePromptText|//@android:contentDescription|//string-array/item/text()'

DEFAULT_XPATH_PATTERN_STRING = '//text()'
XPATH_PATTERN_STRING = '<!--\s*xpath#(.*?)-->'
NAMESPACES_PATTERN_STRING = 'xmlns:(.*?)="(.*?)"'
#pattern = re.compile('<!--xpath#(.*?)-->')
pattern = re.compile(XPATH_PATTERN_STRING)


class XMLWordHandler(WordHandler):

    ext = 'xml'

    def extract(self, content, user_upload=False):
        return self.__parse_xml(content, user_upload)

    def integrate(self, content, word_list, user_upload=False):
        # word_dict = self._word_list_to_dict(word_list)
        # entry_list = []
        # for word in word_list:
        #     entry_list.append(word[1])
        return self.__parse_xml(content, user_upload, word_list)
    
    def __parse_xpath(self, doc, xpath_list, entry_list=None, _namespaces=None):
        """
        :param entry_list: a list store relation of src_words and their translate result, such as [(src1, trans1),(src2, trans2)]
        """
        # 根据给定xpath提取词条
        words_dict = {}
        if entry_list is not None:
            for entry in entry_list:
                words_dict[entry[0]] = entry[1]

        try:
            ret = []
            i = 0
            for xpath_elem in xpath_list:
                xpath_elem = xpath_elem.strip()
                if xpath_elem == "":
                    continue

                path_node = xpath_elem.split("/")
                path_type = path_node[len(path_node) - 1]

                logger.info("XPATH: %s" % (xpath_elem))
                if _namespaces:
                    trans_contents = doc.xpath(xpath_elem, namespaces={_namespaces[0] : _namespaces[1]})
                else:
                    trans_contents = doc.xpath(xpath_elem)
                    
                if path_type == "text()":
                    for trans_content in trans_contents:
                        source = trans_content.getparent().text
                        if not source or not source.strip():
                            continue
                        if source[0] == '@':
                            # 如果要提取的内容是'@string/text'之类的格式，则不进行提取翻译
                            continue
                        source = get_unicode(source.strip())
                        ret.append(source)

                        if entry_list is not None:
                            target, i = self.replace_or_origin(source, i, entry_list, words_dict)

                        # if word_dict is not None and source in word_dict:
                        #     target = word_dict[source]
                            if target is not None:
                                if '<![CDATA[' in etree.tostring(trans_content.getparent()):
                                    trans_content.getparent().text = CDATA(target)
                                else:
                                    trans_content.getparent().text = target
                elif '@' in path_type:
                    for trans_content in trans_contents:
#                        source = trans_content.getparent().get(path_type[1:])
                        source = trans_content
                        if not source or not source.strip():
                            continue
                        if source[0] == '@':
                            # 如果要提取的内容是'@string/text'之类的格式，则不进行提取翻译
                            continue
                        source = get_unicode(source.strip())
                        ret.append(source)

                        target = None
                        target_path_type = None

                        if entry_list is not None:
                            target, i = self.replace_or_origin(source, i, entry_list, words_dict)
                        # if word_dict is not None and source in word_dict:
                        #     target = word_dict[source]
                        if target is not None:
                            target = unescape(target, {'&quot;': '"', '&apos;':'\''})
#                            trans_content.getparent().set(path_type[1:], target)
                            # path_type有可能具有namespace
                            if ':' in path_type:
                                attr = path_type[path_type.find(':')+1 : ]
                                target_path_type = '{' + _namespaces[1] + '}' + attr
                            else:
                                target_path_type = path_type[1:]
                            trans_content.getparent().set(target_path_type, target)

            # if word_dict is not None:
            if entry_list is not None:
                return etree.tostring(doc, encoding="utf-8", xml_declaration=True) #@UndefinedVariable

            if not ret:
                pass
#                print "EmptyXPathContent"

            return ret
        except etree.XPathEvalError:
            pass
#            print "XPathEvalError"
        except etree.XMLSyntaxError, e:
            raise XMLSyntaxError(e)
#            print "XMLSyntaxError"


    def __parse_xml(self, xml_content, user_upload, entry_list=None):
        """
        :param xml_content: content of xml file
        :param entry_list: a list store relation of src_words and their translate result, such as [(src1, trans1),(src2, trans2)]
        :return: if entry_list is none ,return a word list, otherwise ,return a string content after translated
        """
        # 提取词条或回填翻译结果
        if type(xml_content) in (str, unicode):
            st = StringIO.StringIO(xml_content)
        else:
            st = xml_content
            try:
                st.seek(0)
            except:
                pass

        try:
            parser = etree.XMLParser(encoding='utf-8', strip_cdata=False)
            doc = etree.parse(st, parser)
            st.close()

            content = etree.tostring(doc)
            # get the xpath of the xml file
            match = re.search(XPATH_PATTERN_STRING, content)
            
            match_ns = re.search(NAMESPACES_PATTERN_STRING, content)
            ns = None
            if match_ns:
                ns = (match_ns.group(1), match_ns.group(2))
            
            if not match:
                # no xpath
                # try android xpath
                logger.debug("<<<try android xpath>>>")
                xpath_list = ANDROID_XPATH_PATTERN_STRING.split('|')
                ret = self.__parse_xpath(doc, xpath_list, entry_list, _namespaces=('android', ANDROID_NAMESPACES))
                if ret:
                    return ret
                
                # if try-android-xpath failed
                if user_upload:
                    # return all text node
                    logger.debug("<<<from user upload>>>")
                    xpath_list = [DEFAULT_XPATH_PATTERN_STRING]
                else:
                    # return nothing
                    raise NoXPathInfoError()
#                    print "NoXPathInfoError"
            else:
                xpath_list = match.group(1).split('|')

            ret = []
            ret = self.__parse_xpath(doc, xpath_list, entry_list, ns)
            
            if entry_list is not None:
                return etree.tostring(doc, encoding="utf-8", xml_declaration=True) #@UndefinedVariable

            if not ret:
                pass
#                print "EmptyXPathContent"

            return ret
        except etree.XPathEvalError:
            pass
#            print "XPathEvalError"
        except etree.XMLSyntaxError, e:
            raise XMLSyntaxError(e)
#            print "XMLSyntaxError"


xml_word_handler_instance = XMLWordHandler()



if __name__ == '__main__':
    pass
   # filename = "/root/share/test.xml"
   # fread = open(filename, 'r')
   # xml_content = fread.read()
   # fread.close()
   #
   # word_list = xml_word_handler_instance.extract(xml_content, user_upload=True)
   #
   # print '\nword_list:'
   # for word in word_list:
   #     print word
#
#    word_dict_1 = {'version':'vvvv', 'send_me_bugs':'ssss', 'wrap_content':'wwww',
#                   'homepage':'hhhh', 'credits':'ccccc'}
#    word_dict_2 = {u'名字':'name', u'经验':'exp', u'金钱':'money', u'果实':'fruit',
#                   u'购买':'buy', u'播种':'seed', u'浇水':'water', u'收割':'reap',
#                   u'卖出':'sell'}
#    word_dict_3 = {'Everyday Italian':u'每日意大利', 'Harry Potter':u'哈利波特',
#                   'Learning XML':u'学习xml'}
#    new_xml = xml_word_handler_instance.integrate(xml_content, word_dict_3, user_upload=True)
#    
#    print '\nnew_xml:'
#    print new_xml


