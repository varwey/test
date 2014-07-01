# coding=utf-8
from nowdo.controls.notice import Notice
from nowdo.utils.db_migration import create_tables, drop_tables

__author__ = 'lhfu'

tables = [
    Notice,
]


def upgrade():
    create_tables(tables)


def downgrade():
    drop_tables(tables)


if __name__ == "__main__":
    downgrade()
    upgrade()