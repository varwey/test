#!-*- coding:utf8 -*-

from nowdo.controls.file import File, FileStatus
from nowdo.controls.entry import Entry
from nowdo.utils.nowdo_logger import nowdo_logger as logger
from kfile.utils.opencc_wrapper import opencc


class FileImpl(object):
    source = property(lambda self: self.file.source)

    lang = property(lambda self: self.file.lang)

    handler = property(lambda self: self.file.handler)

    session = property(lambda self: self.file.session)

    group_name = property(lambda self: self.file.group_name)

    content = property(lambda self: self.file.content)

    source_type = property(lambda self: self.file.source_type)

    entries = property(lambda self: self.file.entries)

    word_list = property(lambda self: [e.word for e in self.entries])

    def __init__(self, file=None):
        self.file = file

    @property
    def compl_files(self):
        """
        获取所有ComplFile
        """
        return self.session.query(File). \
            filter(File.parent_file_id == self.file.id).all()

    def create_compl_files(self, tar_langs):
        """
        创建ComplFile
        """
        compl_files = []

        new_lang_names = set(tar_langs) - set([f.lang for f in self.compl_files])
        for lang in new_lang_names:
            compl_files.append(self.create_compl_file_for_lang(lang))

        return compl_files

    def create_compl_file_for_lang(self, tar_lang):
        """
        根据TarLang创建ComplFile
        """
        compl_file = File.create(self.session, self.group_name, self.source, tar_lang,
                                 source_type=self.file.source_type,
                                 content_type=self.file.content_type,
                                 parent_file_id=self.file.id,
                                 status=FileStatus.WAITING_FOR_HANDLING)

        # 复制文件内容
        compl_file.update_content(self.file.content)

        return compl_file

    def get_compl_file_by_lang(self, tar_lang):
        return self.session.query(File) \
            .filter(File.parent_file_id == self.file.id) \
            .filter(File.lang == tar_lang).first()

    def extract(self):
        """
        分解OrigFile
        """
        if not self.__validate_extraction():
            return False

        #从原始文件中抽取词汇
        try:
            new_word_list = self.gen_word_list()
            self.insert_word_list([(word, index) for index, word in  enumerate(new_word_list)])
        except Exception, e:
            logger.error("Parse file %s error %s " % (self.source, e))

        return len(new_word_list)

    def __validate_extraction(self):
        if not self.handler:
            logger.error('No handler found for file=%s' % self.file.gridfs_path)
            return False

        if not self.handler.supported:
            logger.debug('Not supported for file=%s' % self.file.gridfs_path)
            for compl_file in self.compl_files:
                compl_file.update_content(self.content)
                compl_file.update_status(FileStatus.NOT_SUPPORTED)

                if compl_file.is_js:
                    # js文件简繁转换
                    if self.lang == 'cn' and compl_file.lang == 'tw':
                        compl_file.update_content(opencc("s2t", self.content))
                        compl_file.update_status(FileStatus.MACHINE_COMPLETE)
                    elif self.lang == 'tw' and compl_file.lang == "cn":
                        compl_file.update_content(opencc("t2s", self.content))
                        compl_file.update_status(FileStatus.MACHINE_COMPLETE)

            self.file.update_status(FileStatus.NOT_SUPPORTED)
            return False

        return True

    def gen_word_list(self):
        """
        抽取词条
        """
        word_handler = self.handler.word_handler
        user_upload = (self.file.source_type == File.UPLOAD_FROM_LOCAL)

        word_list = word_handler.extract(self.content, user_upload=user_upload)

        # 上面是先根据扩展名来提取词条，如果没有提取出词条，则尝试content-type
        if not word_list and hasattr(self.handler, "content_type"):
            word_list = word_handler.extract(self.content, user_upload=user_upload)

        logger.debug('Generating word list finished.')

        # 去掉空白词条
        return [word for word in word_list if word.strip()]

    def insert_word_list(self, word_list):
        """
        插入词条
        """
        Entry.create_multi(word_list, self.file.id, self.group_name)

    def integrate(self, orig_file):
        """
        文件合成
        """
        # 将origfile的内容复制到complfile
        self.file.update_content(orig_file.content)

        # 获取origfile的词条
        # src_entries = dict(entry.get_entries_by_file(orig_file.id, orig_file.group_name))
        temp_src_entries = Entry.get_entries_by_file(orig_file.id, orig_file.group_name)
        src_entries = dict([(t.word, t.position) for t in temp_src_entries])

        # 获取complfile的词条
        temp_tar_entries = Entry.get_entries_by_file(self.file.id, self.file.group_name)
        tar_entries = dict([(t.position, t.word) for t in temp_tar_entries])
        # tar_entries = dict([(item[1], item[0]) for item in ])

        word_list = []
        for entry in src_entries:
            word_list.append((entry, tar_entries.get(src_entries.get(entry), entry)))

        user_upload = (self.file.source_type == File.UPLOAD_FROM_LOCAL)

        # 回填翻译结果
        result_content = self.handler.word_handler.integrate(orig_file.content, word_list, user_upload=user_upload)

        if result_content is not None:
            self.file.update_content(result_content)

        self.file.update_status(FileStatus.MACHINE_COMPLETE)
        orig_file.file_impl.update_status()

    def update_status(self):
        """
        更新OrigFile的状态。
        """
        current_status = self.current_status
        if self.current_status != self.file.status:
            self.file.update_status(current_status)

    @property
    def current_status(self):
        """
        综合所有ComplFile的状态得出OrigFile的状态。
        """
        status_cnt_dict = {}
        for status in (FileStatus.WAITING_FOR_HANDLING, FileStatus.WAITING_FOR_TRANSLATION,
                       FileStatus.NO_WORD, FileStatus.MACHINE_COMPLETE):
            status_cnt_dict[status] = 0

        for compl_file in self.compl_files:
            status = compl_file.status
            if status in status_cnt_dict:
                status_cnt_dict[status] += 1

        if status_cnt_dict[FileStatus.WAITING_FOR_HANDLING] > 0:
            return FileStatus.WAITING_FOR_HANDLING
        if status_cnt_dict[FileStatus.WAITING_FOR_HANDLING] == 0 and \
                status_cnt_dict[FileStatus.WAITING_FOR_TRANSLATION] > 0:
            return FileStatus.WAITING_FOR_TRANSLATION
        if status_cnt_dict[FileStatus.WAITING_FOR_TRANSLATION] == 0 and \
                status_cnt_dict[FileStatus.MACHINE_COMPLETE] > 0:
            return FileStatus.MACHINE_COMPLETE
        if status_cnt_dict[FileStatus.WAITING_FOR_TRANSLATION] == 0 and \
                status_cnt_dict[FileStatus.NO_WORD] > 0:
            return FileStatus.NO_WORD

        return self.file.status