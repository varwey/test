# -*- coding: utf-8 -*-
__author__ = 'yanggaoxiang'
from StringIO import StringIO
def extract(file_content):
    # word_list = []
    # prop_dict = get_dict(get_logical_lines(file_content))
    # for k,v in prop_dict.items():
    #     if v:
    #         word_list.append(v)
    # return word_list
    return [word[1] for word in get_list(get_logical_lines(file_content))]


def integrate(file_content, entry_list):
    translated_file_content = ''
    words_dict = {}
    for entry in entry_list:
        words_dict[entry[0]] = entry[1]

    prop_list = get_list(get_logical_lines(file_content))
    i = 0
    for word in prop_list:
        if i >= len(entry_list):
            translated_file_content += (word[0] + '=' + words_dict.get(word[1], word[1]) + '\n')
        elif entry_list[i][1] is None:
            translated_file_content += (word[0] + '=' + word[1] + '\n')
            i += 1
        elif word[1].strip():
            translated_file_content += (word[0] + '=' + word[1] + '\n')
        else:
            translated_file_content += (word[0] + '=' + entry_list[i][1] + '\n')
            i += 1

    # prop_dict = get_dict(get_logical_lines(file_content))
    # for k,v in prop_dict.items():
    #     if v in word_dict:
    #         translated_file_content += (k + '=' + word_dict[v] + '\n')
    #     else:
    #         translated_file_content += (k + '=' + v + '\n')
    return translated_file_content.encode('utf-8')

def get_logical_lines(file_content):
    result = []
    logical_line = ''
    buf = StringIO(file_content)
    end = True
    for line in buf:
        preceding_backslash = False
        newline = line.lstrip()
        if newline.startswith('!#') and end:
            continue
        for c in newline:
            if c == '\\':
                preceding_backslash = not preceding_backslash
            elif c == '\n' and preceding_backslash:
                print newline
                end = False
            else :
                preceding_backslash = False
        if end:
            logical_line = logical_line + newline
            result.append(logical_line)
            logical_line = ''
        else:
            logical_line = logical_line + newline[:-2]
            end = True
            print logical_line
    return result

def get_list(logical_lines):
    result = []
    for line in logical_lines:
        limit = len(line)
        keylen = 0
        valuestart = limit
        hassep = False
        preceding_backslash = False
        while keylen<limit:
            c = line[keylen]
            if (c == '=' or c == ':') and not preceding_backslash:
                valuestart = keylen + 1
                hassep = True
                break
            elif (c == ' ' or c == '\t' or c == '\f') and not preceding_backslash:
                valuestart = keylen + 1
                break
            if c == '\\':
                preceding_backslash = not preceding_backslash
            else:
                preceding_backslash = False
            keylen += 1
        while valuestart<limit:
            c = line[valuestart]
            if c != ' ' and c != '\t' and c != '\f':
                if not hassep and (c == '=' or c == ':'):
                    hassep = True
                else:
                    break
            valuestart += 1
        key = line[0:keylen]
        value = line[valuestart:]
        if not key == '':
            result.append((key.strip(), value.strip()))
            # result[key.strip()] = value.strip()
    return result

if __name__ == '__main__':
    fs = open('test2.properties')
    file_content = fs.read()
    fs.close()
    a = dict()
    a[u'氢气球'] = u'العربية'
    print a
    print integrate(file_content, a)
    print get_dict(get_logical_lines(file_content))