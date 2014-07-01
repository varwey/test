# coding=utf8
import traceback
from kfile.translation.file.word_handler import WordHandler
import kfile.translation.file.xlsx.translate as translate
from kfile.utils.kfile_logging import logger


class XLSXWordHandler(WordHandler):

    ext = 'xlsx'

    def extract(self, content, user_upload=False):
        """
        content：文件内容。该方法从文件中提取词条。
        """
        try:
            return translate.extract(content)
        except Exception, e:
            logger.error(traceback.format_exc(e))
            return []


    def integrate(self, content, word_list, user_upload=False):
        """
        content：文件内容；word_dict：原词与翻译结果的对应关系。该方法将翻译结果回填到文件。
        返回翻译好的文件内容
        """
        try:
            return translate.integrate(content, word_list)
        except Exception, e:
            logger.error(traceback.format_exc(e))
            return None


xlsx_word_handler_instance = XLSXWordHandler()