#coding:utf8

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    image = url_for('static', filename='img/animal_2.jpg')
    return render_template('index.html', username='varwey', image=image)

if __name__ == '__main__':
    app.debug = True
    app.run(port=12345)
