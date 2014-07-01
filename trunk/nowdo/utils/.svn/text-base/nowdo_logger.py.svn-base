# -*- coding: utf-8 -*-
__author__ = 'lhfu'
from nowdo.config import setting
from nowdo.utils.colored_logging import Logging
from kfile.utils import kfile_logging

nowdo_logger = Logging.get_logger('nowdo', log_level=setting.LOG_LEVEL, log_file=setting.LOG_FILE)
nowdo_celery_logger = Logging.get_logger('nowdo_celery', log_level=setting.LOG_LEVEL, log_file=setting.CELERY_LOG_FILE)

kfile_logging.logger = Logging.get_logger('kfile', log_level=setting.LOG_LEVEL, log_file=setting.LOG_FILE)
kfile_logging.celery_logger = Logging.get_logger('kfile_celery', log_level=setting.LOG_LEVEL, log_file=setting.CELERY_LOG_FILE)