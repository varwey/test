# coding=utf8
"""
词条的分解和合并
"""

import json
import traceback
from kfile.translation.file.json.json_wordhandler import json_word_handler_instance
from Libs.sgmlparser.sgml.html_extract import ExtractHtml
from kfile.translation.file.html.html_wordhandler import html_word_handler_instance
from Libs.strs.coding_util import get_unicode
from Libs.strs.opencc_wrapper import opencc
from kfile.utils.kfile_logging import logger


class Word(object):

    # 词条的类型
    WORD_PLAIN, WORD_JSON, WORD_XML = range(3)


    def __init__(self, word):
        self.word = word


    def extract(self, USE_FINE_GRAINED_TRANS=True):
        """
        分解词条得到各个片段（姑且称之为sub words）
        :return: sub words list
        """
        if not USE_FINE_GRAINED_TRANS:
            return [self.word]

        return self.__parse()


    def integrate(self, sub_word_dict, USE_FINE_GRAINED_TRANS=True):
        """
        由各个片段的翻译结果合并成总的翻译结果
        :param sub_word_dict:
        :return: translate result
        """
        if not USE_FINE_GRAINED_TRANS:
            return sub_word_dict.get(self.word, None)

        u_sub_word_dict = dict()
        u_sub_word_dict.update([(get_unicode(k), get_unicode(v)) for k, v in sub_word_dict.items()])

        return self.__parse(u_sub_word_dict)


    def __parse(self, sub_word_dict=None):
        word_type = self.type

        if word_type == Word.WORD_JSON:
            ret = self.__parse_json_word(sub_word_dict)
        elif word_type == Word.WORD_XML:
            ret = self.__parse_xml_word(sub_word_dict)
        else:
            ret = self.__parse_plain_word(sub_word_dict)

        return ret


    def __parse_json_word(self, sub_word_dict=None):
        """
        json词条的分解、合并
        :param sub_word_dict:
        :return:
        """
        sub_words = []  #子词条
        result = None   #翻译结果
        try:
            if sub_word_dict is not None:   # 合并
                result = json_word_handler_instance.integrate(self.word, sub_word_dict)
            else:   # 分解
                sub_words = list(set([elem for elem in json_word_handler_instance.extract(self.word)
                                 if elem.strip()]))
        except Exception, e:
            logger.warn(traceback.format_exc(e))
            sub_words = [self.word]
            result = self.word

        if sub_word_dict is not None:
            return result
        else:
            return sub_words


    def __parse_xml_word(self, sub_word_dict=None):
        """
        xml词条的分解、合并
        :param sub_word_dict:
        :return:
        """
        sub_words = []  #子词条
        result = None   #翻译结果
        try:
#            we = WordExtractor(get_unicode(self.word))
#
#            if sub_word_dict is not None:   # 合并
#                result = we.insert_words(sub_word_dict)
#            else:   # 分解
#                sub_words = list(set([elem for elem in we.extract_words() if elem.strip()]))

            u_word = get_unicode(self.word)
            if sub_word_dict is not None:
                result = html_word_handler_instance.integrate(u_word, sub_word_dict)
            else:
                sub_words = html_word_handler_instance.extract(u_word)
        except Exception, e:
            logger.warn(traceback.format_exc(e))
            sub_words = [self.word]
            result = self.word

        if sub_word_dict is not None:
            return result
        else:
            return sub_words


    def __parse_plain_word(self, sub_word_dict=None):
        """
        纯文本词条
        :param sub_word_dict:
        :return:
        """
        if sub_word_dict is not None:
            # 如果没有找到则翻译结果为None
            return sub_word_dict.get(get_unicode(self.word), None)

        return [self.word]


    @property
    def type(self):
        """
        词条的类型
        :return:
        """
        ret = Word.WORD_PLAIN
        if self.__is_json:
            ret = Word.WORD_JSON
        elif self.__is_xml:
            ret = Word.WORD_XML

        return ret


    @property
    def __is_xml(self):
        """
        判断词条是否是xml字符串（非严格的xml）
        """
        ret = False
        try:
#            we = WordExtractor(get_unicode(self.word))
#            segments = we.get_segments()
            segments = ExtractHtml().get_segments(get_unicode(self.word))
            for segment in set([elem for elem in segments if elem.strip()]):
                if segment.startswith('<') and segment.endswith('>'):
                    ret = True
                    break
        except Exception, e:
            logger.warn(traceback.format_exc(e))

        return ret


    @property
    def __is_json(self):
        """
        判断词条是否是json字符串
        """
        ret = False
        try:
            data = json.loads(get_unicode(self.word))
            if type(data) in (dict, list):
                ret = True
        except ValueError:
            pass
        except Exception, e:
            logger.warn(traceback.format_exc(e))

        return ret


def translate_word_by_opencc(word, src_lang, tar_lang, USE_FINE_GRAINED_TRANS=True):
    """
    opencc简繁转换翻译词条
    :param word:
    :return: 如果不能翻译则返回None，否则返回简繁转换的结果
    """
    # 事先判断，快速返回
    LANG_CN = "cn"; LANG_TW = "tw"
    if src_lang not in (LANG_CN, LANG_TW) or tar_lang not in (LANG_TW, LANG_CN):
        return None

    w = Word(word)
    sub_words = w.extract(USE_FINE_GRAINED_TRANS)
    sub_word_dict = dict()

    for sw in sub_words:
        if isinstance(sw, unicode):
            sw = sw.encode("utf8")

        # opencc接受的参数类型、返回值都是str类型
        result = None
        if src_lang == LANG_CN and tar_lang == LANG_TW:
            result = opencc("s2t", sw)
        elif src_lang == LANG_TW and tar_lang == LANG_CN:
            result = opencc("t2s", sw)
        if result is not None:
            sub_word_dict[sw] = result

    return w.integrate(sub_word_dict, USE_FINE_GRAINED_TRANS)



def type_test():
    # normal string
    word0 = u"hello, world"
    word1 = u"你好，世界"
    # the following string should not be judged as json string although they pass json.loads
    word6 = u"null"
    word7 = u"false"
    word8 = u"true"
    word9 = u"1234"
    word10 = u"12.34"
    # json string
    word2 = u"""{"text": "你好，世界"}"""
    word3 = u"""[{"text": "你好，世界"}]"""
    # xml string
    word4 = u"你好<font>world"
    word5 = u"hello<unknown>世界"

    assert Word(word0).type == Word.WORD_PLAIN
    assert Word(word1).type == Word.WORD_PLAIN
    assert Word(word2).type == Word.WORD_JSON
    assert Word(word3).type == Word.WORD_JSON
    assert Word(word4).type == Word.WORD_XML
    assert Word(word5).type == Word.WORD_XML
    assert Word(word6).type == Word.WORD_PLAIN
    assert Word(word7).type == Word.WORD_PLAIN
    assert Word(word8).type == Word.WORD_PLAIN
    assert Word(word9).type == Word.WORD_PLAIN
    assert Word(word10).type == Word.WORD_PLAIN


def extract_test():
    # normal string
    word0 = u"""During the campaign, as long as it is to the level of the corresponding totem, can obtain corresponding pay return, order time is high, the more revenue. (command center at level 30 open totem system)"""
    word1 = u"""1.每次对悬赏对象造成伤害即可获得现金，伤害越多，获得现金越多。2.使用军饷消除冷却扣除2军饷（不论剩余时长）。3.伤害排名前5的玩家，分别获得赏金的20%、      15%、10%、3%、2%；且分别获得声望50、40、30、20、10。4.对悬赏对象造成最后一击的玩家获得赏金的50%，声望50。5.最后一击和排名的奖励需要在通缉页面领取，有效领取时间为悬赏对象死亡一天内。"""
    # json string
    word2 = u"""{"clz":"PutonEquip2QuestGuide","params":{"text":{"step1":"双击装备"},"equip_id":12,"step0":"hud@bagButton","msg":{"step1":{"c":"双击手枪即可装备，装备是提升战斗力的基本途径之一。","y":227,"x":237}},"tip":"打开背包"}}"""
    # json list
    word3 = u"""[{"text":"感谢将军的救命之恩。","dir":2,"role":3,"type":"role"},{"text":"各位受苦了，军如此，国之哀！你们赶紧离开吧。","role":1,"type":"role"},{"text":"政府军已经如此，哪里还有我们容身之地啊？我等愿投效将军，重建家园。","dir":2,"role":3,"type":"role"}]"""
    # xml string
    word4 = u"""<font color='#339900'>  <u>   <a href='event:u${uid}'>${uname}</a></u></font>在竞技场中与你挑战,成功将你当成垫脚石踢了下去,你的当前名次为${rating}。<font color='#339900'><u><a href='event:athletics'>竞技场</a></u></font>"""
    word5 = u"""1，酒馆任务分为 <font color='#ffffff'>白</font>, <font color='#4EF424'>绿</font>, <font color='#51F7F7'>蓝</font>, <font color='#845CF9'>紫</font>, <font color='#FF9900'>橙</font> 五个不同颜色的"""

    for word in (word0, word1, word2, word3, word4, word5):
        w = Word(word)
        print w.type
        for sw in w.extract():
            print sw
        print '\r'


def integrate_test():
    # normal string
    word0 = u"""During the campaign, as long as it is to the level of the corresponding totem, can obtain corresponding pay return, order time is high, the more revenue. (command center at level 30 open totem system)"""
    word1 = u"""1.每次对悬赏对象造成伤害即可获得现金，伤害越多，获得现金越多。2.使用军饷消除冷却扣除2军饷（不论剩余时长）。3.伤害排名前5的玩家，分别获得赏金的20%、      15%、10%、3%、2%；且分别获得声望50、40、30、20、10。4.对悬赏对象造成最后一击的玩家获得赏金的50%，声望50。5.最后一击和排名的奖励需要在通缉页面领取，有效领取时间为悬赏对象死亡一天内。"""
    # json string
    word2 = u"""{"clz":"PutonEquip2QuestGuide","params":{"text":{"step1":"双击装备"},"equip_id":12,"step0":"hud@bagButton","msg":{"step1":{"c":"双击手枪即可装备，装备是提升战斗力的基本途径之一。","y":227,"x":237}},"tip":"打开背包"}}"""
    # json list
    word3 = u"""[{"text":"感谢将军的救命之恩。","dir":2,"role":3,"type":"role"},{"text":"各位受苦了，军如此，国之哀！你们赶紧离开吧。","role":1,"type":"role"},{"text":"政府军已经如此，哪里还有我们容身之地啊？我等愿投效将军，重建家园。","dir":2,"role":3,"type":"role"}]"""
    # xml string
    word4 = u"""<font color='#339900'>  <u>   <a href='event:u${uid}'>${uname}</a></u></font>在竞技场中与你挑战,成功将你当成垫脚石踢了下去,你的当前名次为${rating}。<font color='#339900'><u><a href='event:athletics'>竞技场</a></u></font>"""
    word5 = u"""1，酒馆任务分为 <font color='#ffffff'>白</font>, <font color='#4EF424'>绿</font>, <font color='#51F7F7'>蓝</font>, <font color='#845CF9'>紫</font>, <font color='#FF9900'>橙</font> 五个不同颜色的"""

    import random, string

    for word in (word0, word1, word2, word3, word4, word5):
        w = Word(word)
        print w.type
        sub_word_dict = dict()
        for sw in w.extract():
            result = ''.join([random.choice(string.letters + string.digits) for i in range(10)])
            sub_word_dict[sw] = result
        print w.integrate(sub_word_dict)


def test_css():
    word = u"""<p><style type="text/css">p{ width:650px; margin:0 auto; line-height:26px; font-size:11px;} </style></p><p>hello, world    <br />  你好吗？  how are you</p>"""
    w = Word(word)
    print w.type
    print w.extract()

    import random, string
    sub_word_dict = {}
    for sw in w.extract():
        result = ''.join([random.choice(string.letters + string.digits) for i in range(10)])
        sub_word_dict[sw] = result
    print w.integrate(sub_word_dict)


if __name__ == '__main__':
    test_css()
    type_test()
    extract_test()
    integrate_test()
#    word = '<html>hello测试hello</html>'
#    w = Word(word)
#    sub_word_dict = dict()
#    for sw in w.extract():
#        print sw
#        sub_word_dict[sw] = sw + 'translated'
#
#    print w.integrate(sub_word_dict)