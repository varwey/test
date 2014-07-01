# -*- coding: utf-8 -*-
import re
from Libs.strs.word_filter import is_hash
cm_ = re.compile(r"^(g\d+)|(\d|\s|USD|AUD|BRL|CAD|EUR|GBP|INR|PHP|RUB|SEK|M|kg|cm|￥|\*|\-|/|~|\(|\)|\.|\$)+$")

txt = 'http://docs.python.org/2/library/functools.html'

url_regex = '((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))$'    # HTTP URL 1

rg = re.compile(url_regex, re.IGNORECASE)
m = rg.search(txt)
if m:
    httpurl1 = m.group(1)
    print "(" + httpurl1 + ")" + "\n"

def need_translation(word):
    _word = word.strip()
    if '| part Last(msg_question_cat)' in _word:
        return False
    if re.match(url_regex, _word): # url
    #        print word, 'is url'
        return False
    if re.match(cm_, _word):
    #        print word, 'is rubbish'
        return False
    if is_hash(_word):
        return False
    return True


def test_reg():
    t_words = [
        "straight",
        "Hockey Jersey",
        "6 --- 9",
        "Other Sports &amp; Outdoors",
        "Indoor Sporting Goods",
        "Exercise & Fitness Equipment",
        "Athletic Footwear",
        "USD 16.55 ~ USD 34.17",
        "Football Jersey",
        "Other Sports & Outdoors",
        "Children's Sporting Goods",
        "Free Shipping aero pro Drive TENNIS RACKET RACQUET 1pcs on TradeTang.com",
        " USD 56.93 ~ USD 57.75 ",
        "0.980 (kg)",
        "Free Shipping aero pro Drive TENNIS RACKET RACQUET 1pcs",
        "USD 51.75 ~ USD 67.98",
        "Drama DVD",
        " USD 258.75 ",
        "Sci-Fi & Fantasy DVD",
        " 11017",
        "Price (lot ( 5 Pieces per lot))",
        " 2010-08-31",
        "USD 51.75 ~ USD 61.54",
        "97.3 ",
        "USD 258.75 ~ USD 307.72",
        "wholesale 5pcs Charmed Season 1-8 1 2 3 4 5 6 7 8 49 DVD Boxset US version 009 on TradeTang.com",
        "Documentary DVD",
        " USD 289.80 ~ USD 307.72 ",
        "Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version with BOOK In Stock 1",
        " USD 53.82 ",
        "Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version with BOOK In Stock 1 on TradeTang.com",
        " USD 70.98 ~ USD 73.58 ",
        "USD 53.82 ~ USD 73.58",
        "Free DHL 20pcs/lot Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version1 ",
        " USD 750.38 ",
        "DHL",
        "USD 36.23 ~ USD 38.55",
        " USD 724.50 ",
        " USD 771.08 ",
        "25.000 (kg)",
        "Free DHL 20pcs/lot Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version1 on TradeTang.com",
        "USD 724.50 ~ USD 771.08",
        "MySQL server error report:Array ( [0] => Array ( [message] => MySQL Query Error ) [1] => Array ( [sql] => insert into `vogueinchina`.`v_ip_limited_times`(ip,first_time,times) values('119.254.245.114','2012-11-16 15:23:00','1') ) [2] => Array ( [error] => Duplicate entry '119.254.245.114' for key 1 ) [3] => Array ( [errno] => 1062 ) ) ",
        " USD 35.74 ~ USD 36.32 ",
        " USD 25.88 ~ USD 26.55 ",
        " New Charmed The complete season 1-8 48DVD 8individual Boxset US version 1 on TradeTang.com",
        " USD 31.50 ~ USD 33.42 ",
        "USD 25.88 ~ USD 36.32",
        " New Charmed The complete season 1-8 48DVD 8individual Boxset US version 1",
        " USD 72.45 ~ USD 75.46 ",
        "Free shipping the Charmed The Complete Series Season 1-8 48DVD boxset DVD 222",
        " USD 81.38 ~ USD 84.75 ",
        "Free shipping the Charmed The Complete Series Season 1-8 48DVD boxset DVD 222 on TradeTang.com",
        " USD 62.10 ",
        "USD 62.10 ~ USD 84.75",
        " USD 507.15 ",
        "Free DHL Charmed The complete season 1-8 48DVD 8individual Boxset US version 1",
        "USD 507.15 ~ USD 567.10",
        "Free DHL Charmed The complete season 1-8 48DVD 8individual Boxset US version 1 on TradeTang.com",
        " USD 533.03 ",
        " USD 533.03 $",
        "http://www.cnblogs.com/sislcb/archive/2008/12/15/1355481.html ",
        "http://www.cnblogs.com/sislcb/archive/2008/12/15/1355481.html fuck",
        " http://www.cnblogs.com/sislcb/archive/2008/12/15/1355481.html ",
        "RUB 83.50 ~ 178.61",
        "INR 148.04 ~ 316.68",
        "AUD 2.59 ~ 5.55",
        "CAD 2.68 ~ 5.72",
        "PHP 1537.22 ~ 1784.71",
        "EUR 28.98 ~ 33.65",
        "SEK 249.93 ~ 290.17",
        "CAD 37.26 ~ 43.26",
        "BRL 79.42 ~ 92.21",
        "GBP 23.34 ~ 27.09",
        "EUR 131.57 ~ 156.06",
        "CAD 169.16 ~ 200.65",
        "RUB 5278.17 ~ 6260.79",
        "AUD 164.04 ~ 194.57",
        "SEK 1134.58 ~ 1345.80",
        "GBP 105.94 ~ 125.66",
        "BRL 360.54 ~ 427.65",
        "PHP 6978.33 ~ 8277.45",
        """    Welcome to Tmart! Tmart aims to facilitate your work and delight your life. We are proud to provide you with a wide selection of products at low prices. Here you’ll find electronics such as digital photo frames, chargers, laser pointers, flashlights, cell phones, car accessories, cameras, game accessories and more. Enjoy your shopping here and take your favorite products home at a competitive price with worldwide free shipping! We also make every effort to offer you efficient and comprehensive customer service. If you encounter a problem, ourresponsive and professional customer service team is always ready to help you. Tmart hopes to become your friend!""",
        "23.8"
    ]
    words_need_translation = [word for word in t_words if need_translation(word)]
    print words_need_translation
    words_dont_need_translation = filter(lambda s: not need_translation(s), t_words)
    print 'X:', words_dont_need_translation
    print 100.0 * len(words_dont_need_translation) / len(t_words), "%"
    _target = ['straight', 'Hockey Jersey', 'Other Sports &amp; Outdoors', 'Indoor Sporting Goods',
               'Exercise & Fitness Equipment', 'Athletic Footwear', 'Football Jersey', 'Other Sports & Outdoors',
               "Children's Sporting Goods", 'Free Shipping aero pro Drive TENNIS RACKET RACQUET 1pcs on TradeTang.com',
               'Free Shipping aero pro Drive TENNIS RACKET RACQUET 1pcs', 'Drama DVD', 'Sci-Fi & Fantasy DVD',
               'Price (lot ( 5 Pieces per lot))',
               'wholesale 5pcs Charmed Season 1-8 1 2 3 4 5 6 7 8 49 DVD Boxset US version 009 on TradeTang.com',
               'Documentary DVD', 'Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version with BOOK In Stock 1',
               'Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version with BOOK In Stock 1 on TradeTang.com',
               'Free DHL 20pcs/lot Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version1 ', 'DHL',
               'Free DHL 20pcs/lot Charmed Season 1-8 1 2 3 4 5 6 7 8 48 DVD Boxset US version1 on TradeTang.com',
               "MySQL server error report:Array ( [0] => Array ( [message] => MySQL Query Error ) [1] => Array ( [sql] => insert into `vogueinchina`.`v_ip_limited_times`(ip,first_time,times) values('119.254.245.114','2012-11-16 15:23:00','1') ) [2] => Array ( [error] => Duplicate entry '119.254.245.114' for key 1 ) [3] => Array ( [errno] => 1062 ) ) ",
               ' New Charmed The complete season 1-8 48DVD 8individual Boxset US version 1 on TradeTang.com',
               ' New Charmed The complete season 1-8 48DVD 8individual Boxset US version 1',
               'Free shipping the Charmed The Complete Series Season 1-8 48DVD boxset DVD 222',
               'Free shipping the Charmed The Complete Series Season 1-8 48DVD boxset DVD 222 on TradeTang.com',
               'Free DHL Charmed The complete season 1-8 48DVD 8individual Boxset US version 1',
               'Free DHL Charmed The complete season 1-8 48DVD 8individual Boxset US version 1 on TradeTang.com',
               'http://www.cnblogs.com/sislcb/archive/2008/12/15/1355481.html fuck',         """    Welcome to Tmart! Tmart aims to facilitate your work and delight your life. We are proud to provide you with a wide selection of products at low prices. Here you’ll find electronics such as digital photo frames, chargers, laser pointers, flashlights, cell phones, car accessories, cameras, game accessories and more. Enjoy your shopping here and take your favorite products home at a competitive price with worldwide free shipping! We also make every effort to offer you efficient and comprehensive customer service. If you encounter a problem, ourresponsive and professional customer service team is always ready to help you. Tmart hopes to become your friend!"""]

    assert words_need_translation == _target

    assert words_dont_need_translation == ['6 --- 9', 'USD 16.55 ~ USD 34.17', ' USD 56.93 ~ USD 57.75 ', '0.980 (kg)',
                                           'USD 51.75 ~ USD 67.98', ' USD 258.75 ', ' 11017', ' 2010-08-31',
                                           'USD 51.75 ~ USD 61.54', '97.3 ', 'USD 258.75 ~ USD 307.72',
                                           ' USD 289.80 ~ USD 307.72 ', ' USD 53.82 ', ' USD 70.98 ~ USD 73.58 ',
                                           'USD 53.82 ~ USD 73.58', ' USD 750.38 ', 'USD 36.23 ~ USD 38.55',
                                           ' USD 724.50 ', ' USD 771.08 ', '25.000 (kg)', 'USD 724.50 ~ USD 771.08',
                                           ' USD 35.74 ~ USD 36.32 ', ' USD 25.88 ~ USD 26.55 ',
                                           ' USD 31.50 ~ USD 33.42 ', 'USD 25.88 ~ USD 36.32',
                                           ' USD 72.45 ~ USD 75.46 ', ' USD 81.38 ~ USD 84.75 ', ' USD 62.10 ',
                                           'USD 62.10 ~ USD 84.75', ' USD 507.15 ', 'USD 507.15 ~ USD 567.10',
                                           ' USD 533.03 ', ' USD 533.03 $',
                                           'http://www.cnblogs.com/sislcb/archive/2008/12/15/1355481.html ',
                                           ' http://www.cnblogs.com/sislcb/archive/2008/12/15/1355481.html ',
                                           'RUB 83.50 ~ 178.61', 'INR 148.04 ~ 316.68', 'AUD 2.59 ~ 5.55',
                                           'CAD 2.68 ~ 5.72', 'PHP 1537.22 ~ 1784.71', 'EUR 28.98 ~ 33.65',
                                           'SEK 249.93 ~ 290.17', 'CAD 37.26 ~ 43.26', 'BRL 79.42 ~ 92.21',
                                           'GBP 23.34 ~ 27.09', 'EUR 131.57 ~ 156.06', 'CAD 169.16 ~ 200.65',
                                           'RUB 5278.17 ~ 6260.79', 'AUD 164.04 ~ 194.57', 'SEK 1134.58 ~ 1345.80',
                                           'GBP 105.94 ~ 125.66', 'BRL 360.54 ~ 427.65', 'PHP 6978.33 ~ 8277.45', "23.8"]


if __name__ == '__main__':
    test_reg()