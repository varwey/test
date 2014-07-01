# coding=utf-8

# author = "hhl"

def replace_or_origin(src_word, index, entry_list, words_dict={}):
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