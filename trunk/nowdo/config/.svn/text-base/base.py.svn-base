# -*- coding:utf-8 -*-
import os

__author__ = 'SL'

SECRET_KEY = 'cooperation translate platform key'

DEBUG = True
ECHO_SQL = False

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")

VERSION = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION'), 'r').read()

TASK_FILE_GROUP_STR = 'now_do_task_file'
AVATAR_FILE_GROUP_STR = 'now_do_avatar_file'

OFFICIAL_ACCOUNT = 'sunlei@xingcloud.com'

# CAS Config
CAS_ENABLE = False
CAS_SERVER_URL = "http://passport.xingcloud.com"

DEFAULT_INIT_LOCALE = 'zh_CN'

SUPPORTED_LANGUAGES_FULL = {
    # u'ar': {u'cn_name': '阿拉伯语', u'price': 400, u'code': u'ar', u'name': u'العربية', u'lang_trans': u'لغة',
    #         u'flag_url': u'/static/images/flag/ar.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'cn': {u'cn_name': '简体中文', u'price': 150, u'code': u'cn', u'name': u'简体中文', u'lang_trans': u'语言',
            u'flag_url': u'/static/images/flag/cn.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'de': {u'cn_name': '德语', u'price': 400, u'code': u'de', u'name': u'Deutsch', u'lang_trans': u'Sprache',
            u'flag_url': u'/static/images/flag/de.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'en': {u'cn_name': '英语', u'price': 250, u'code': u'en', u'name': u'English', u'lang_trans': u'Language',
            u'flag_url': u'/static/images/flag/en.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'fr': {u'cn_name': '法语', u'price': 400, u'code': u'fr', u'name': u'Français', u'lang_trans': u'langue',
            u'flag_url': u'/static/images/flag/fr.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'it': {u'cn_name': '意大利语', u'price': 400, u'code': u'it', u'name': u'Italiano', u'lang_trans': u'lingua',
    #         u'flag_url': u'/static/images/flag/it.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'ja': {u'cn_name': '日语', u'price': 300, u'code': u'ja', u'name': u'日本語', u'lang_trans': u'言語',
            u'flag_url': u'/static/images/flag/ja.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'ko': {u'cn_name': '韩语', u'price': 300, u'code': u'ko', u'name': u'한국의', u'lang_trans': u'언어',
            u'flag_url': u'/static/images/flag/ko.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'nl': {u'cn_name': '荷兰语', u'price': 450, u'code': u'nl', u'name': u'Nederlands', u'lang_trans': u'taal',
    #         u'flag_url': u'/static/images/flag/nl.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'pl': {u'cn_name': '波兰语', u'price': 400, u'code': u'pl', u'name': u'Polski', u'lang_trans': u'język',
    #         u'flag_url': u'/static/images/flag/pl.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'pt': {u'cn_name': '葡萄牙语', u'price': 400, u'code': u'pt', u'name': u'Português', u'lang_trans': u'linguagem',
    #         u'flag_url': u'/static/images/flag/pt.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'ru': {u'cn_name': '俄语', u'price': 400, u'code': u'ru', u'name': u'Pусский', u'lang_trans': u'язык',
            u'flag_url': u'/static/images/flag/ru.jpg', u'human': True, u'machine': True, u'crowd': True},
    u'es': {u'cn_name': '西班牙语', u'price': 400, u'code': u'es', u'name': u'Español', u'lang_trans': u'idioma',
            u'flag_url': u'/static/images/flag/es.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'th': {u'cn_name': '泰语', u'price': 350, u'code': u'th', u'name': u'ภาษาไทย', u'lang_trans': u'ภาษา',
    #         u'flag_url': u'/static/images/flag/th.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'tw': {u'cn_name': '繁体中文', u'price': 150, u'code': u'tw', u'name': u'繁體中文', u'lang_trans': u'語言',
    #         u'flag_url': u'/static/images/flag/tw.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'tr': {u'cn_name': '土耳其语', u'price': 400, u'code': u'tr', u'name': u'Türk', u'lang_trans': u'dil',
    #         u'flag_url': u'/static/images/flag/tr.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'no': {u'cn_name': '挪威语', u'price': 500, u'code': u'no', u'name': u'Norsk', u'lang_trans': u'språk',
    #         u'flag_url': u'/static/images/flag/no.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'sv': {u'cn_name': '瑞典语', u'price': 500, u'code': u'sv', u'name': u'Svenska', u'lang_trans': u'Språk',
    #         u'flag_url': u'/static/images/flag/sv.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'vi': {u'cn_name': '越南语', u'price': 300, u'code': u'vi', u'name': u'Việt', u'lang_trans': u'ngôn ngư',
    #         u'flag_url': u'/static/images/flag/vi.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'id': {u'cn_name': '印尼语', u'price': 450, u'code': u'id', u'name': u'Indonesia', u'lang_trans': u'bahasa',
    #         u'flag_url': u'/static/images/flag/id.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'fi': {u'cn_name': '芬兰语', u'price': 500, u'code': u'fi', u'name': u'Suomi', u'lang_trans': u'kieli',
    #         u'flag_url': u'/static/images/flag/fi.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'da': {u'cn_name': '丹麦语', u'price': 500, u'code': u'da', u'name': u'Dansk', u'lang_trans': u'sprog',
    #         u'flag_url': u'/static/images/flag/da.jpg', u'human': True, u'machine': True, u'crowd': True},
    # u'el': {u'cn_name': '希腊语', u'code': u'el', u'name': u'ελληνικά', u'lang_trans': u'γλώσσα',
    #         u'flag_url': u'/static/images/flag/el.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'hu': {u'cn_name': '匈牙利语', u'code': u'hu', u'name': u'Magyar', u'lang_trans': u'nyelv',
    #         u'flag_url': u'/static/images/flag/hu.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'af': {u'cn_name': '南非荷兰语', u'code': u'af', u'name': u'Afrikaans', u'lang_trans': u'taal',
    #         u'flag_url': u'/static/images/flag/af.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'sq': {u'cn_name': '阿尔巴尼亚语', u'code': u'sq', u'name': u'Shqiptar', u'lang_trans': u'gjuhë',
    #         u'flag_url': u'/static/images/flag/sq.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'be': {u'cn_name': '白俄罗斯语', u'code': u'be', u'name': u'Беларускія', u'lang_trans': u'мова',
    #         u'flag_url': u'/static/images/flag/be.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'bg': {u'cn_name': '保加利亚语', u'code': u'bg', u'name': u'български', u'lang_trans': u'език',
    #         u'flag_url': u'/static/images/flag/bg.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'ca': {u'cn_name': '加泰罗尼亚语', u'code': u'ca', u'name': u'Català', u'lang_trans': u'Idioma',
    #         u'flag_url': u'/static/images/flag/ca.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'hr': {u'cn_name': '克罗地亚语', u'code': u'hr', u'name': u'Hrvatski', u'lang_trans': u'jezik',
    #         u'flag_url': u'/static/images/flag/hr.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'cs': {u'cn_name': '捷克语', u'code': u'cs', u'name': u'český', u'lang_trans': u'jazyk',
    #         u'flag_url': u'/static/images/flag/cs.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'et': {u'cn_name': '爱沙尼亚语', u'code': u'et', u'name': u'Eesti', u'lang_trans': u'keel',
    #         u'flag_url': u'/static/images/flag/et.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'tl': {u'cn_name': '菲律宾语', u'code': u'tl', u'name': u'Pilipino', u'lang_trans': u'wika',
    #         u'flag_url': u'/static/images/flag/tl.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'gl': {u'cn_name': '加利西亚语', u'code': u'gl', u'name': u'Galicia', u'lang_trans': u'linguaxe',
    #         u'flag_url': u'/static/images/flag/gl.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'iw': {u'cn_name': '希伯来语', u'code': u'iw', u'name': u'עברית', u'lang_trans': u'שפה',
    #         u'flag_url': u'/static/images/flag/iw.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'hi': {u'cn_name': '印地语', u'code': u'hi', u'name': u'हिंदी', u'lang_trans': u'भाषा',
    #         u'flag_url': u'/static/images/flag/hi.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'is': {u'cn_name': '冰岛语', u'code': u'is', u'name': u'Icelandic', u'lang_trans': u'tungumál',
    #         u'flag_url': u'/static/images/flag/is.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'ga': {u'cn_name': '爱尔兰语', u'code': u'ga', u'name': u'Gaeilge', u'lang_trans': u'teanga',
    #         u'flag_url': u'/static/images/flag/ga.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'lv': {u'cn_name': '拉托维亚语', u'code': u'lv', u'name': u'Latvijas', u'lang_trans': u'valoda',
    #         u'flag_url': u'/static/images/flag/lv.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'lt': {u'cn_name': '立陶宛语', u'code': u'lt', u'name': u'Lietuvos', u'lang_trans': u'kalba',
    #         u'flag_url': u'/static/images/flag/lt.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'mk': {u'cn_name': '马其顿语', u'code': u'mk', u'name': u'македонски', u'lang_trans': u'јазик',
    #         u'flag_url': u'/static/images/flag/mk.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'ms': {u'cn_name': '马来语', u'code': u'ms', u'name': u'Melayu', u'lang_trans': u'bahasa',
    #         u'flag_url': u'/static/images/flag/ms.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'mt': {u'cn_name': '马耳他语', u'code': u'mt', u'name': u'Malti', u'lang_trans': u'lingwa',
    #         u'flag_url': u'/static/images/flag/mt.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'fa': {u'cn_name': '波斯语', u'code': u'fa', u'name': u'فارسی', u'lang_trans': u'زبان',
    #         u'flag_url': u'/static/images/flag/fa.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'ro': {u'cn_name': '罗马尼亚语', u'code': u'ro', u'name': u'Român', u'lang_trans': u'limbă',
    #         u'flag_url': u'/static/images/flag/ro.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'sr': {u'cn_name': '塞尔维亚语', u'code': u'sr', u'name': u'Cрпски', u'lang_trans': u'језик',
    #         u'flag_url': u'/static/images/flag/sr.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'sk': {u'cn_name': '斯洛伐克语', u'code': u'sk', u'name': u'Slovenčina', u'lang_trans': u'jazyk',
    #         u'flag_url': u'/static/images/flag/sk.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'sl': {u'cn_name': '斯洛文尼亚语', u'code': u'sl', u'name': u'Slovenski jezik', u'lang_trans': u'Jezik',
    #         u'flag_url': u'/static/images/flag/sl.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'sw': {u'cn_name': '斯瓦希里语', u'code': u'sw', u'name': u'Kiswahili', u'lang_trans': u'lugha',
    #         u'flag_url': u'/static/images/flag/sw.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'uk': {u'cn_name': '乌克兰语', u'code': u'uk', u'name': u'Український', u'lang_trans': u'Мова',
    #         u'flag_url': u'/static/images/flag/uk.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'cy': {u'cn_name': '威尔士语', u'code': u'cy', u'name': u'Cymraeg', u'lang_trans': u'iaith',
    #         u'flag_url': u'/static/images/flag/cy.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'yi': {u'cn_name': '意第绪语', u'code': u'yi', u'name': u'ייִדיש', u'lang_trans': u'שפּראַך',
    #         u'flag_url': u'/static/images/flag/yi.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'eo': {u'cn_name': '世界语', u'code': u'eo', u'name': u'Esperanto', u'lang_trans': u'lingvo',
    #         u'flag_url': u'/static/images/flag/eo.jpg', u'human': False, u'machine': True, u'crowd': True},
    # u'ht': {u'cn_name': '海地克里奥尔语', u'code': u'ht', u'name': u'Haitian Creole', u'lang_trans': u'Lang',
    #         u'flag_url': u'/static/images/flag/ht.jpg', u'human': False, u'machine': True, u'crowd': True}
}