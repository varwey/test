# coding=utf8
import traceback

from kfile.utils.kfile_logging import logger
from kfile.translation.file.word_handler import WordHandler
from kfile.translation.file.xls import translate


class XLSWordHandler(WordHandler):

    ext = 'xls'

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
        content：文件内容；word_list：原词与翻译结果的对应关系。该方法将翻译结果回填到文件。
        返回翻译好的文件内容
        """
        # word_dict = self._word_list_to_dict(word_list)
        try:
            return translate.integrate(content, word_list)
        except Exception, e:
            logger.error(traceback.format_exc(e))
            return None


xls_word_handler_instance = XLSWordHandler()