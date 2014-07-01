#coding=utf8
__author__ = 'T510'


import re
#utf8编码转换
currency_pattern = re.compile("(\+|\-)?\s*(US|CA|€|£|AU|SGD|NOK|CHF|HK|BRL\s*R|R)?\s*(\$|￥)\s*([\.\-,0-9\s]*)$", re.I)

contain_currency_pattern = re.compile("(\+|\-)?\s*(US|CA|€|£|AU|SGD|NOK|CHF|HK|BRL\s*R|R)?\s*(\$|￥)\s*([\.\-,0-9\s]*)", re.I)


def pure_currency(data):
    '''
    @param data: 待检测数据
    @return: 是否是货币字符串
    '''
    t_data = data
    if isinstance(t_data, unicode):
        t_data = t_data.encode('utf-8')
    if re.match(currency_pattern, t_data):
        #完全是一个货币字符串
        return True
    else:
        return False


def contain_currency(data):
    '''
    @param data: 待检测数据
    @return: 检测结果, 模板字符串, 货币字符串
    '''
    t_data = data
    if isinstance(t_data, unicode):
        t_data = t_data.encode('utf-8')
    matObj = re.search(contain_currency_pattern, t_data)
    if matObj:
        return True, t_data.replace(matObj.group(0), ''), matObj.group(0)
    else:
        return False, None, None


if __name__ == '__main__':
    print pure_currency("-US$ 0.42")
    text = "the price is: + US$ 5.8, and so all"
    print contain_currency(text)