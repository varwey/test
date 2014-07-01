# -*- coding: utf-8 -*-

import polib
import StringIO
from babel.messages.pofile import read_po, write_po
from Libs.strs.coding_util import get_unicode
from kfile.utils.translate.file_integrate import replace_or_origin


def extract(file_content):
    buf = StringIO.StringIO(file_content)
    catalog = read_po(buf)
    word_list = []
    for msg in catalog:
        if not msg.id == '':
            word_list.append(msg.id)
    return word_list


def extract_new(content):
    content = get_unicode(content)
    po = polib.pofile(content)

    words = []
    # 只提取还没有翻译的词条
    for entry in po.untranslated_entries():
        msgid_strip = entry.msgid.strip()
        msgid_plural_strip = entry.msgid_plural.strip()
        if msgid_strip:
            words.append(msgid_strip)
        if msgid_plural_strip:
            words.append(msgid_plural_strip)

    return words


def integrate_new(content, entry_list):
    """
        :param entry_list: a list store relation of src_words and their translate result, such as [(src1, trans1),(src2, trans2)]
    """
    words_dict = {}
    for entry in entry_list:
        words_dict[entry[0]] = entry[1]

    content = get_unicode(content)
    po = polib.pofile(content)
    i = 0
    for entry in po.untranslated_entries():
        msgid_strip = entry.msgid.strip()
        msgid_plural_strip = entry.msgid_plural.strip()

        if msgid_strip:
            tar_word, i = replace_or_origin(msgid_strip, i, entry_list, words_dict)
            r = entry.msgid.replace(msgid_strip, tar_word)
        if msgid_plural_strip:
            tar_word, i = replace_or_origin(msgid_plural_strip, i, entry_list, words_dict)
            r_plural = entry.msgid_plural.replace(msgid_plural_strip, tar_word)

        # r = entry.msgid.replace(msgid_strip, word_dict.get(msgid_strip, msgid_strip))
        # r_plural = entry.msgid_plural.replace(msgid_plural_strip, word_dict.get(msgid_plural_strip, msgid_plural_strip))

        if msgid_plural_strip:  # 如果有msgid_plural
            d = entry.msgstr_plural
            print d
            for key in d.keys():
                if key == u"0":
                    if not d[key]:
                        entry.msgstr_plural[key] = r
                else:
                    if not d[key]:
                        entry.msgstr_plural[key] = r_plural
        else:
            if not entry.msgstr:
                entry.msgstr = r

    # this will call po object's __unicode__ method
    # just like what is done internally in po.save()
    return unicode(po).encode("utf-8")


def integrate(file_content, word_dict):
    read_buf = StringIO.StringIO(file_content)
    catalog = read_po(read_buf)
    catalog.charset = 'utf-8'
    for msg in catalog:
        if msg.id in word_dict:
            msg.string = word_dict[msg.id]
    write_buf = StringIO.StringIO()
    write_po(write_buf, catalog)
    translated_file_content = write_buf.getvalue()
    return translated_file_content


if __name__ == '__main__':
    import os
    from kfile.utils.fileUtil import read_file, write_file

    test_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    po_test_dir = os.path.join(test_dir, "tests", "po")

    content = read_file(os.path.join(po_test_dir, "de.po"))
    print "length of orig content: %d"%len(content)
    words = extract_new(content)

    for word in words:
        assert type(word) == unicode

    print "extract %d words"%len(words)

    # word_dict = dict()
    word_list = []
    for word in words:
        # word_dict[word] = word + u"translated"
        word_list.append((word, word + u"translated"))

    new_content = integrate_new(content, word_list)
    print len(new_content)
    write_file(new_content, os.path.join(po_test_dir, "result.po"))