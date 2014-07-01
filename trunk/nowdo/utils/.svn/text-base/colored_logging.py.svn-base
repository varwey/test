#coding=utf8
"""
Created on 2011-9-25

@author: of
"""
import logging


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        level_name = record.levelname
        if self.use_color and level_name in COLORS:
            level_name_color = COLOR_SEQ % (30 + COLORS[level_name]) + level_name + RESET_SEQ
            record.levelname = level_name_color
        return logging.Formatter.format(self, record)


class Logging:

    def __init__(self):
        pass

    @staticmethod
    def get_logger(name=__name__, log_level="debug", log_file=None):
        ## get log level.
        log_level = Logging.get_log_level(log_level)

        ## create logger
        logger_instance = logging.getLogger(name)
        
        ## create log handler.
        if len(logger_instance.handlers) <= 0:
            if log_file is not None:
                handler = logging.FileHandler(log_file)
            else:
                handler = logging.StreamHandler()
                
            formatter = ColoredFormatter("%(asctime)s\t"
                                         "%(process)d|%(thread)d\t"
                                         "%(levelname)s\t"
                                         "%(module)s\t"
                                         "%(funcName)s:%(lineno)d\t"
                                         "%(message)s", "%Y-%m-%d@%H:%M:%S")
            handler.setFormatter(formatter)

            logger_instance.addHandler(handler)
            logger_instance.setLevel(log_level)
        
        return logger_instance

    @staticmethod
    def get_log_level(log_level):
        log_level = getattr(logging, log_level.upper(), None)
        if log_level is None:
            raise Exception("No such log level.")
        return log_level

if __name__ == '__main__':
    logger = Logging.get_logger(log_level="debug")
    
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    logger.setLevel(Logging.get_log_level("error"))

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    
    ## The output looks like this:
    # 2011-05-26@13:54:05    10006|-1215969600    DEBUG    testLogger    <module>:33    debug message
    # 2011-05-26@13:54:05    10006|-1215969600    INFO    testLogger    <module>:34    info message
    # 2011-05-26@13:54:05    10006|-1215969600    WARNING    testLogger    <module>:35    warn message
    # 2011-05-26@13:54:05    10006|-1215969600    ERROR    testLogger    <module>:36    error message
    # 2011-05-26@13:54:05    10006|-1215969600    CRITICAL    testLogger    <module>:37    critical message
    # 2011-05-26@13:54:05    10006|-1215969600    ERROR    testLogger    <module>:45    error message
    # 2011-05-26@13:54:05    10006|-1215969600    CRITICAL    testLogger    <module>:46    critical message