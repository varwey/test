# coding=utf-8


class FileStatus(object):

    DOWNLOADING = 0             # 正在下载
    WAITING_FOR_HANDLING = 1    # 等待处理
    WAITING_FOR_TRANSLATION = 2 # 等待翻译
    MACHINE_COMPLETE = 3        # 机器翻译完成
    NOT_SUPPORTED = 4           # 不支持
    NO_WORD = 5                 # 无词汇
    DELETING = 6                # 正在删除

    SWF_EXTRACT_EXCEPTION = 51  # SWF文件分解异常