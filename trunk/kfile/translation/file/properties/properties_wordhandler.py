# coding=utf-8
__author__ = 'yanggaoxiag'

from kfile.translation.file.word_handler import WordHandler
from Libs.strs.coding_util import get_unicode
import kratos.translation.file.properties.translate as translate

class PROPERTIESWordHandler(WordHandler):

    ext = 'properties'

    def extract(self, content, user_upload=False):
        content = get_unicode(content)
        return translate.extract(content)

    def integrate(self, content, word_list, user_upload=False):
        # word_dict = self._word_list_to_dict(word_list)
        content = get_unicode(content)
        return translate.integrate(content, word_list)

properties_word_handler_instance = PROPERTIESWordHandler()