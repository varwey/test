# coding=utf-8
"""
created by SL on 14-3-5
"""
from nowdo.controls.reg_invitation import RegInvitation
from nowdo.utils.db_migration import create_tables, drop_tables

__author__ = 'SL'

tables = [
    RegInvitation,
]


def upgrade():
    create_tables(tables)


def downgrade():
    drop_tables(tables)


if __name__ == "__main__":
    # downgrade()
    upgrade()