# coding=utf-8
from nowdo import application as app

__author__ = 'SL'
# app = create_app()

if __name__ == '__main__':
    # print app.url_map
    app.run(debug=True, host='0.0.0.0', port=5050)
