#coding=utf8
#__author__="hhl"

from kratos.setting import WORD_TASK_RECEIVE_URL, WORD_TASK_GET_URL, KRATOS_DEFAULT_PRIORITY, \
    KRATOS_API_PRIORITY, WRITE_WORDS_FROM_WORD_TASK, KRATOS_MODULE_ID, KRATOS_API_MODULE_ID
import requests
from kratos.utils.logger import kr_logger as logger
import traceback


def get_from_word_task(word_task_id):
    try:
        data = {
                "id": word_task_id,
            }
        return requests.post(WORD_TASK_GET_URL, data).content

    except Exception, e:
        logger.error(traceback.format_exc(e))
        return

