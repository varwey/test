#coding=utf8
__author__ = 'hhl'

from nowdo.controls.file_impl import *

# 注册file_impl
File.register_file_impl(FileImpl)

# 注册file_handler
from kfile.translation.file.json.json_filehandler import JSONFileHandler
from kfile.translation.file.xml.xml_filehandler import XMLFileHandler
from kfile.translation.file.html.html_filehandler import HTMLFileHandler, HTMFileHandler
# from kfile.translation.file.css.css_filehandler import CSSFileHandler
from kfile.translation.file.xls.xls_filehandler import XLSFileHandler
from kfile.translation.file.xlsx.xlsx_filehandler import XLSXFileHandler
from kfile.translation.file.po.po_filehandler import POFileHandler
from kfile.translation.file.properties.properties_filehandler import PROPERTIESFileHandler
from kfile.translation.file.csv.csv_filehandler import CSVFileHandler
from kfile.translation.file.txt.txt import TXTFileHandler
from kfile.translation.file.ini.ini import INIFileHandler
from kfile.translation.file.docx.docx_filehandler import DocxFileHandler
from kfile.translation.file.pptx.pptx_filehandler import PptxFileHandler

File.register_file_handler([JSONFileHandler, XMLFileHandler,
                            HTMLFileHandler, XLSFileHandler,
                            POFileHandler, PROPERTIESFileHandler, CSVFileHandler,
                            HTMFileHandler, TXTFileHandler, INIFileHandler,
                            XLSXFileHandler, DocxFileHandler, PptxFileHandler])