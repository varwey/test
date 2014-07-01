# coding=utf-8
from nowdo.controls.account import Account
from nowdo.controls.account_property import AccountProperty
from nowdo.utils.db_migration import create_tables, drop_tables

__author__ = 'lhfu'

tables = [
    Account,
    AccountProperty,
]


def upgrade():
    create_tables(tables)


def downgrade():
    drop_tables(tables)


if __name__ == "__main__":
    # downgrade()
    upgrade()