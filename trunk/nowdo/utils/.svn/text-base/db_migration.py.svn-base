# -*- coding: utf-8 -*-
import contextlib
from sqlalchemy.exc import ProgrammingError
from nowdo.controls.base import metadata, main_db_engine

__author__ = 'yeshiming@gmail.com'

# 以下操作db1到db4

import traceback
from sqlalchemy import MetaData, Table, Column, Index
from migrate import * # 必须，会monkeypatch sqlalchemy函数


def create_tables(cls_list):
    u"""创建表"""
    print 'Creating table on', main_db_engine
    table_list = []
    for cls in cls_list:
        table = cls
        if not isinstance(cls, Table):
            table = cls.__table__
        table_list.append(table)
    metadata.create_all(bind=main_db_engine, tables=table_list)


def drop_tables(cls_list):
    u"""删除表"""
    print 'Dropping table on', main_db_engine
    table_list = []
    for cls in cls_list:
        table = cls
        if not isinstance(cls, Table):
            table = cls.__table__
        table_list.append(table)
    metadata.drop_all(bind=main_db_engine, tables=table_list)


def create_table(cls):
    u"""创建表"""
    print 'Creating table on', main_db_engine
    table = cls
    if not isinstance(cls, Table):
        table = cls.__table__
    metadata.create_all(bind=main_db_engine, tables=[table])


def drop_table(cls):
    u"""循环所有数据库删除表"""
    print 'Creating table on', main_db_engine
    table = cls
    if not isinstance(cls, Table):
        table = cls.__table__
    metadata.drop_all(bind=main_db_engine, tables=[table])


def create_index(table, index_name, col_name):
    u"""为表某个字段创建索引"""
    try:
        i = Index(index_name, getattr(table.c, col_name))
        print 'creating index', i
        i.create(bind=table.metadata.bind)
    except:
        print traceback.format_exc()


def drop_index(table, index_name, col_name):
    u"""为表某个字段删除索引"""
    try:
        i = Index(index_name, getattr(table.c, col_name))
        print 'dropping index', i
        i.drop(bind=table.metadata.bind)
    except:
        print traceback.format_exc()


def create_column(table, col, **kwargs):
    u"""为表某个表增加字段"""
    try:
        assert type(table) is str
        print 'creating col', col
        table = get_table(table)
        col.create(table, **kwargs)
    except Exception, e:
        print traceback.format_exc(e)


def alter_column(table_name, col, **kwargs):
    u"""
        修改某个表中字段的属性
    """
    try:
        assert type(col) is str
        assert type(table_name) is str
        table = get_table(table_name)
        print '>> altering col: %s of table: %s' % (col, str(table))
        print getattr(table.c, col).alter(**kwargs)
    except AssertionError:
        print 'col and table_name should be a str type'
    except Exception, e:
        print traceback.format_exc(e)


def drop_column(table, col):
    u"""为表某个表增删除段"""
    try:
        assert type(table) is str
        print 'dropping col: ', col
        table = get_table(table)
        col.drop(table)
    except:
        print traceback.format_exc()


def get_table(table_name):
    u"""通过表名在数据库中获得表对象"""
    meta = MetaData()
    meta.bind = main_db_engine
    table = Table(table_name, meta, autoload=True)
    return table


def clear_data(table_name):
    table = get_table(table_name)
    with contextlib.closing(main_db_engine.connect()) as con:
        trans = con.begin()
        print 'clear all data in table: %s' % str(table)
        con.execute(table.delete())
        trans.commit()


def clear_all_data():
    # meta = MetaData()
    # meta.bind = main_db_engine
    with contextlib.closing(main_db_engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            if str(table) not in ['account_property', 'account', 'router', 'group']:
                try:
                    print 'clear all data in table: %s' % str(table)
                    con.execute(table.delete())
                except ProgrammingError:
                    print traceback.format_exc()
                    continue
        trans.commit()
    clear_data('group')


def add_foreign_key(from_table_name, to_table_name, from_column, to_column):
    print 'add_foreign_key:', from_table_name, to_table_name, from_column, to_column
    meta = MetaData(bind=main_db_engine)
    from_table = Table(from_table_name, meta, autoload=True)
    to_table = Table(to_table_name, meta, autoload=True)

    try:
        foreign_key = ForeignKeyConstraint([getattr(from_table.c, from_column)],
                                           [getattr(to_table.c, to_column)])
        foreign_key.create()

    except Exception, e:
        traceback.format_exc()
        print 'error', e


def drop_foreign_key(from_table_name, to_table_name, from_column, to_column):
    print 'drop_foreign_key:', from_table_name, to_table_name, from_column, to_column
    meta = MetaData(bind=main_db_engine)
    from_table = Table(from_table_name, meta, autoload=True)
    to_table = Table(to_table_name, meta, autoload=True)

    try:
        foreign_key = ForeignKeyConstraint([getattr(from_table.c, from_column)],
                                           [getattr(to_table.c, to_column)])
        foreign_key.drop()

    except Exception, e:
        traceback.format_exc()
        print 'error', e
