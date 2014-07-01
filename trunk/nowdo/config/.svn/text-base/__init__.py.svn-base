# -*- coding:utf-8 -*-
from nowdo.config import production, development, testing, production_test

__author__ = 'zouyingjun'

__all__ = ['setting']

setting = development

import os

current_evn = os.environ.get("NOWDO_ENV") or "development"

if current_evn in ['production']:
    setting = production
elif current_evn in ['development']:
    setting = development
elif current_evn in ['production_test']:
    setting = production_test
elif current_evn in ['testing']:
    setting = testing
else:
    setting = development

del development
del production
del testing
del production_test

print "current_env = %s " % current_evn
