# coding=utf-8
__author__ = 'yanggaoxiang'

from kfile.translation.file.word_handler import WordHandler
from Libs.strs.coding_util import get_unicode
import kfile.translation.file.csv.translate as translate

class CSVWordHandler(WordHandler):

    ext = 'csv'

    def extract(self, content, user_upload=False):
        content = get_unicode(content)
        return translate.extract(content)

    def integrate(self, content, word_list, user_upload=False):
        # word_dict = self._word_list_to_dict(word_list)
        content = get_unicode(content)
        return translate.integrate(content, word_list)

csv_word_handler_instance = CSVWordHandler()