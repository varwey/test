# -*- coding:utf-8 -*-
from flask.ext.script import Manager
from nowdo import application as app
from nowdo.config import setting
from nowdo.controls.group import Group
from nowdo.utils.db_migration import clear_all_data

__author__ = 'SL'

# app = create_app()
manager = Manager(app)

#
# @manager.command
# def server():
#     app.run(debug=True, host='0.0.0.0', port=5050)


@manager.command
def show_config():
    for key in sorted(dir(setting)):
        if key.isupper():
            print key, '=', getattr(setting, key)


@manager.command
def clear_db():
    """
    清空数据库，慎用！！！
    """
    clear_all_data()

if __name__ == '__main__':
    manager.run()
