#-*- coding=utf-8 -*-
#------------html handle常量--------------#

FILTER_TAG = ['style']                                # 过滤的标签
ATTR_WORD_LIST = ['title','alt','placeholder']        # 需要翻译的文字属性
# xc_  开头的meta name 其content 会翻译
ATTR_LINK_LIST = ['src', 'href', 'action','init-src'] # 需要翻译的连接属性
ATTR_LOCAL_LIST = ['xc_local']

TEXT_CONSTRAIN_ATTR = ['currencycode']


IGNORE_TAG =['br']              # 文本翻译忽略翻译此类标签中的文本
NOT_TRANS_TAG = "xc_no_trans"   # on & off 例如： xc_no_trans="on" 子节点默认继承父节点的此类属性
ATTR_ON = "on"                  # 启用此标签属性    不翻译
ATTR_OFF = "off"                # 不启用此标签属性   翻译
NOT_CDN_URL = "xc_no_cdn"       # on & off





# #
import re
DEFAULT_BUM_TRANS_RULE = re.compile("(\+|\-)?\s*(AUD|AED|CAD|CLP|COP|BRL||USD|US|CA|EGP|€|£|AU|SGD|SAR|NOK|CHF|HK|PEN|BRL\s*R|R|RUB|EUA|EUR|MXN|ZAR)?\s*(\$|￥|£|R|€)?\s*([\.\-,0-9\s]*)$", re.I)

DEFAULT_INVALID_WORD_RULE = re.compile(r'[0-9\./,:\-;\+\*%\?!&\$\(\)_#=~\'"@<>\s]+$')

#此页面是否需要本地化reg
DEFAULT_LOCALIZE_FLAG_RULE = re.compile("(xc_local|xc_no_trans)\s*=",re.IGNORECASE)