# coding=utf8
'''
Created on Sep 19, 2012

@author: harveyang
'''
import re
import urlparse
import traceback
from kfile.utils.kfile_logging import logger
from kfile.utils.req_url_parser import parse_req_addr
from kfile.utils.url_reconstruct_util import _add_xcv
from Libs.strs.coding_util import str2utf8
from nowdo.controls.file import File
from kfile.translation.file.file_handler import FileHandler
from kfile.translation.file.css.css_wordhandler import css_word_handler_instance



class CSSFileHandler(FileHandler):

    supported = True
    word_handler = css_word_handler_instance
    ext = 'css'
    content_type = 'text/css'

    url_pattern = re.compile(u"url\s*?\([\'\"]?([\s|\S]*?)[\'\"]?\)")


    def integrate(self, local_aux_file_dict):
        """
        返回合并后的文件的内容
        """
        content = self.base_file.content
        try:
            '''屏蔽简单的上传的css文件'''
            addr = self.base_file.source
            if len(addr.split("/")) == 1 and addr.split(".")[-1] == "css":
                return content
        except Exception, e:
            logger.error(traceback.format_exc(e))
            return content
        content = str2utf8(content)[0].decode("utf-8")
        try:
            tmp_content = re.sub(self.url_pattern, self.replace_background_url, content)
            return str2utf8(tmp_content)[0]
        except Exception, e:
            logger.error(traceback.format_exc(e))
            return content


    def replace_background_url(self, matchobj):
        content = matchobj.group(0)
        content = str2utf8(content)[0]
        url = matchobj.group(1).strip()
        url = str2utf8(url)[0]
        css_file_url = self.base_file.req_addr
        url_part = parse_req_addr(css_file_url)
        group_name = url_part["group_name"]
        lang = url_part["lang"]
        if url_part["source"].startswith("http"):
            source_url = url_part["source"]
        else:
            source_url = "http://" + url_part["source"]
        #获得绝对地址
        new_url = urlparse.urljoin(source_url, url).replace("../", "")
        #添加版本号
        f = File.get_file_by_source_and_lang(self.base_file.session,
                                new_url.split("//")[-1].lstrip("/"),
                                lang, self.base_file.service)
        if f is not None:
            new_url = _add_xcv(new_url, f.full_version_no)
#            new_url = str2utf8(new_url)[0]
        else:
            new_url = _add_xcv(new_url, "0")
        new_url = str2utf8(new_url)[0]

        #拼出相对于cdn的绝对路径
        new_url = (new_url.split("//")[-1]).lstrip("/")
        new_url = "/" + "/".join([group_name, lang, new_url])
        return content.replace(url, new_url)
    
    
if __name__ == "__main__":
    tmp_obj = CSSFileHandler()
    testdict = {}
    testdict["css_file"] = '''.two{background:url(../images/tabs-line.gif) 192px top repeat-y #c7c7c7;height:1px;font-size:0px;}.three{background:url(../images/tabs-line.gif) 296px top repeat-y #c7c7c7;height:1px;font-size:0px;}.four{background:url(../images/tabs-line.gif) 445px top repeat-y #c7c7c7;height:1px;font-size:0px;}.five{background:url(../images/tabs-line.gif) 520px top repeat-y #c7c7c7;height:1px;font-size:0px;}'''
    print tmp_obj.integrate(testdict)