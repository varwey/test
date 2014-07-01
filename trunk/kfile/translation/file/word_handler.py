# coding=utf-8

class WordHandler(object):

    def extract(self, content, user_upload=False):
        """
        content：文件内容。该方法从文件中提取词条。
        """
        return []

    def integrate(self, content, word_dict, user_upload=False):
        """
        content：文件内容；word_dict：原词与翻译结果的对应关系。该方法将翻译结果回填到文件。
        返回翻译好的文件内容
        """
        return None

    def _word_list_to_dict(self, word_list):
        """
        :word_list:  a list which is composite of tuple, such as [(src1, tar1),(src2, tar2),...]
        """
        word_dict = {}
        for word in word_list:
            word_dict[word[0]] = word[1]

        return word_dict

    def replace_or_origin(self, src_word, index, entry_list, words_dict={}):
        """
        :param entry_list: a list store relation of src_words and their translate result, such as [(src1, trans1),(src2, trans2)]
        """
        if not words_dict:
            for entry in entry_list:
                words_dict[entry[0]] = entry[1]

        if index >= len(entry_list):
            tar_word = words_dict.get(src_word, src_word)
        elif entry_list[index] is None:
            tar_word = src_word
        elif not src_word.strip():
            return src_word, index
        else:
            if entry_list[index][0] == src_word:
                tar_word = entry_list[index][1]
            else:
                tar_word = words_dict.get(src_word, src_word)
        return tar_word, index+1