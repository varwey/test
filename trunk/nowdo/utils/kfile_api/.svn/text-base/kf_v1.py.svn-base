#!-*- coding:utf8 -*-

from Libs.mime_types.mime_types import guess_type
from Libs.strs.coding_util import str2utf8
from kfile.utils.paginator import SQLAlchemyPaginator

"""
文件翻译流程：
1、创建源文件
2、创建子文件
3、分解源文件
4、获取词条
5、翻译
6、回写翻译结果
7、合成子文件
"""

from nowdo.utils.session import session_cm
from nowdo.controls.file import File, FileStatus
from nowdo.controls.entry import Entry
from nowdo.utils.nowdo_logger import nowdo_logger as logger


def create_orig_file(session, group_name, source, src_lang, content):
    """
    创建源文件
    Return origin file object
     : group_name: group name which file belong , such as service_name
     : source : file path, such as text.txt
     : src_lang: language of file
     : content: file content
    """
    content = str2utf8(content)[0]
    source_without_params = source.partition("?")[0]
    content_type = guess_type(source_without_params, strict=False)[0]

    logger.debug("create orig file. group_name:%s, source:%s, src_lang:%s, content_type:%s"
                 % (group_name, source, src_lang, content_type))

    orig_file = File.create(session, group_name, source, src_lang, content_type=content_type)
    orig_file.update_content(content)

    return orig_file


def create_compl_files(file_id, tar_langs):
    """
    创建子文件
    Return a list of compl file object
     : file_id : id of origin file
     : tar_langs:  a list of target language which need create compl file
    """
    with session_cm() as session:
        orig_file = session.query(File).get(file_id)

        logger.debug("create compl file. file_id:%s, tar_lang:%s"
                     % (orig_file.id, tar_langs))

        return orig_file.create_compl_files(tar_langs)


def update_content(file_id, content):
    """
    更新源文件内容
     : file_id: id of origin file
     : content : new content of file
    """
    content = str2utf8(content)[0]
    with session_cm() as session:
        orig_file = session.query(File).get(file_id)

        logger.debug("update content. file.id:%s" % orig_file.id)

        orig_file.update_content(content)
    return True

def extract(file_id):
    """
    分解源文件
    : id of origin file
    """
    with session_cm() as session:
        orig_file = session.query(File).get(file_id)

        logger.debug("file extract. file.id:%s" % orig_file.id)

        count = orig_file.extract()
        orig_file.count = count
        session.commit()
    return True


def integrate(file_id, lang):
    """
    文件合成
     : file_id : id of origin file
     : lang: target language which need create compl file
    """
    with session_cm() as session:
        orig_file = session.query(File).get(file_id)

        logger.debug("file integrate. file.id:%s, file.lang:%s, lang:%s"
                     % (orig_file.id, orig_file.lang, lang))

        #获取的是子文件
        if orig_file.lang == lang:
            for compl_file in orig_file.compl_files:
                compl_file.integrate(orig_file)
        else:
            compl_file = orig_file.get_compl_file_by_lang(lang)
            compl_file.integrate(orig_file)
    return True


def delete(file_id):
    """
    删除文件
    : file_id: id of origin file
    """
    with session_cm() as session:
        orig_file = session.query(File).get(file_id)
        file_ids = [file_id]
        if orig_file:
            file_ids.extend([compl_file.id for compl_file in orig_file.compl_files])

            for file_id in file_ids:
                Entry.del_multi(file_id)

            File.delete_multi_by_ids(orig_file.group_name, file_ids)
            logger.debug("file delete. file.id:%s, file_ids:%s" % (orig_file.id, file_ids))
    return True

def get_word_list(group_name, file_id):
    """
    获取词条
    Return a list entry object
    : group_name: group name which file belong , such as service_name
    : file_id: id of origin file
    """
    return Entry.get_entries_by_file(file_id, group_name)


def fill_word_list(file_id, lang, word_list, is_cover=True):
    """
    回写翻译结果
    : file_id: id of origin file
    : lang: target language which need create compl file
    : word_list:  a list of word tuple, such as [(word1, postion1), (word2, postion2)]
    : is_cover: 重新插入/更新词条
    """
    with session_cm() as session:
        compl_file = session.query(File) \
            .filter(File.parent_file_id == file_id) \
            .filter(File.lang == lang).first()

        if is_cover:
            # 重新插入
            compl_file.insert_word_list(word_list)
        else:
            # 更新词条
            Entry.update_entry(compl_file.id, compl_file.group_name, word_list)
    return True


def get_file(file_id, lang):
    """
    获取文件内容
    Return file object
    : file_id: id of origin file
    : lang: target language which need create compl file
    """
    with session_cm() as session:
        file = session.query(File).get(file_id)

        logger.debug("get content. file.id:%s, file.lang:%s, lang:%s"
                     % (file.id, file.lang, lang))

        #获取的是子文件
        if file.lang != lang:
            file = file.get_compl_file_by_lang(lang)

    return file


def get_files(group_name, lang, order='', page=1, size=20):
    """
    获取项目所有文件
    Return a list file object
    : group_name: group name which file belong , such as service_name
    : lang: target language which need create compl file
    """
    with session_cm() as session:
        ORDER_METHODS = {
            '+path': File.source.desc(),
            '-path': File.source,
            '+modification': File.modified_date.desc(),
            '-modification': File.modified_date
        }
        order = ORDER_METHODS.get(order, None)

        query = session.query(File) \
            .filter(File.group_name == group_name) \
            .filter(File.lang == lang) \
            .filter(File.status != FileStatus.DELETING) \
            .order_by(order)

        size = 0 < size < 100 and size or 20

        paginator = SQLAlchemyPaginator(query, size)

        page = 0 < page <= paginator.num_pages and page or paginator.num_pages

        logger.debug("get files. group_name:%s, lang:%s, order:%s, page:%s, size:%s"
                     % (group_name, lang, order, page, size))

        files = paginator.page(page).query.all()
    return files

def get_part_entries(group_name, file_id, entry_id_list):
    """
    获取部分原文件词条
    Return a list entry object
    : group_name: group name which file belong , such as service_name
    :file_id : origin file id
    :entry_id_list: a list of entry id
    """
    if not isinstance(entry_id_list, list) or not entry_id_list:
        return []

    return Entry.get_part_entries(file_id, entry_id_list)


def get_entries(group_name, lang, file_id='', order='', page=1, size=20):
    """
    获取所有词条
    Return a list entry object
    : group_name: group name which file belong , such as service_name
    : lang: target language which need create compl file
    """
    size = 0 < size < 100 and size or 20
    page = 0 < page and page or 1

    with session_cm() as session:
        #查询文件
        query = session.query(File) \
            .filter(File.group_name == group_name) \
            .filter(File.lang == lang) \
            .filter(File.count != 0) \
            .filter(File.status != FileStatus.DELETING)

        if file_id:
            file = session.query(File).get(file_id)
            if file.lang != lang:
                file = file.get_compl_file_by_lang(lang)
            query = query.filter(File.id == file.id)

        files = query.order_by(File.id).all()

        # 查找词条所在的文件id
        entries = []
        count = 0
        start, end = (page - 1) * size, page * size
        for file in files:
            if count <= start <= count + file.count or count <= end <= count + file.count or \
                    (count > start and count + file.count < end):

                offset = start - count if count <= start <= count + file.count else 0
                limit = size - len(entries)

                entries.extend(Entry.get_entries(group_name, file.id, order, offset, limit))
            count = count + file.count

    return entries