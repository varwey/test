# -*- coding: utf-8 -*-
import traceback
from nowdo.utils.session import session_cm
from nowdo.config.celeryconfig import celery
from nowdo.utils.nowdo_logger import nowdo_celery_logger as logger
from nowdo.utils.kfile_api import kf_v1 as kf
from nowdo.controls.crowd_source_task import CrowdSourceTask

__author__ = 'lhfu'


@celery.task(ignore_result=True)
def extract_worker(group_id, file_id, tar_langs=None):
    """
    :param service_id:
    :param file_id: orig_file's id
    分解文件
    """
    logger.debug('Inside Extract Worker: group_id=%s, file_id=%s' % (group_id, file_id))
    try:
        kf.create_compl_files(file_id, tar_langs)
        kf.extract(file_id)

        entries = kf.get_word_list(str(group_id), file_id)
        entry_count = len(entries)
        word_count = 0
        for entry in entries:
            word_count += entry.word_count

        with session_cm() as db_session:
            crowd_source_task = db_session.query(CrowdSourceTask).filter(CrowdSourceTask.file_id == file_id).first()
            crowd_source_task.entry_count = entry_count
            crowd_source_task.word_count = word_count

            db_session.commit()

    except:
        logger.debug(traceback.format_exc())

    logger.debug('Leave Extract Worker: group_id=%s, file_id=%s' % (group_id, file_id))