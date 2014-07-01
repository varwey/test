'''
Created on 2012-1-19

@author: onfire
'''
import subprocess
import commands
import os

from kfile.utils.kfile_logging import logger
from Libs.strs.coding_util import get_unicode


class ShellCaller(object):
    '''
    Handles calls of shell, in Windows or in Linux. 
    
    Usage: 
    sc = ShellCaller('java')
    sc['jar'] = toolAddr
    sc['swf'] = path
    sc['Extract'] = ""
    '''
    
    def __init__(self, program):
        self.program = program
        self.params = ""
    
        
    command = property(lambda self: (self.program + self.params).replace('\\', '/'))
    
    
    def __setitem__(self, key, value):
        self.params += ' -%s %s' % (key, value)
        
    def run(self):
        logger.debug(self.command)
        if os.name == 'nt':
            pipe = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            self.message = pipe.stdout.read()
            self.error = pipe.stderr.read()
            return get_unicode(self.message + self.error)
        else:
            return commands.getoutput(self.command)
        
if __name__ == '__main__':
    sc = ShellCaller('java')
    sc.run()