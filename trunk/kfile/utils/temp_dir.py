"""
Created on 2011-12-29
@author: onfire

"""

from kfile import setting
import os
import posixpath
import time
import random


class TempDir(object):
    
    def __init__(self):
        global c
        if not os.path.exists(setting.TEMP_DIR):
            os.makedirs(setting.TEMP_DIR)
        self.dir_name = posixpath.join(setting.TEMP_DIR, str(time.time()) + str(random.random()))
        os.mkdir(self.dir_name)
        
    def __enter__(self, *args, **kwargs):
        return self.dir_name
    
    def __exit__(self, *args, **kwargs):
        #shutil.rmtree(self.dirname)
        pass