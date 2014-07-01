# coding=utf-8

import traceback
from kfile.translation.file.word_handler import WordHandler
import kfile.translation.file.po.translate as translate
from kfile.utils.kfile_logging import logger


class POWordHandler(WordHandler):

    ext = 'po'

    def extract(self, content, user_upload=False):
#        content = get_unicode(content)
#        return translate.extract(content)
        try:
            return translate.extract_new(content)
        except Exception:
            logger.error(traceback.format_exc())
            return []

    def integrate(self, content, word_list, user_upload=False):
#        content = get_unicode(content)
#        return translate.integrate(content, word_dict)
#         word_dict = self._word_list_to_dict(word_list)
        try:
            return translate.integrate_new(content, entry_list=word_list)
        except Exception:
            logger.error(traceback.format_exc())
            return None


po_word_handler_instance = POWordHandler()