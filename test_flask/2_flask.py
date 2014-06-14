#coding:utf8

from flask import Flask, render_template
from itertools import cycle

app = Flask(__name__)

username = cycle([u'张三', u'李四', u'王五', u'赵六'])

@app.route('/')
def index():
    nav_list = {u'首页': [u'轮播大图', u'小广告', u'滚动要闻'],
                u'经济': [u'经济座谈', u'会经济新闻', u'经济与生活'],
                u'文化': [u'农村文化', u'城镇文化', u'文化差异'],
                u'科技': [u'自动化', u'机械工程', u'计算机技术'],
                u'军事': [u'陆军', u'海军', u'空军'],
                u'娱乐': [u'明星', u'游戏', u'综艺']
               }
    return render_template('index.html', nav_list=nav_list, username=username.next())

if __name__ == '__main__':
    app.run(port=12345, debug=True)

