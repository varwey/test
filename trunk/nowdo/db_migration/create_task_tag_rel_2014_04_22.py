# coding=utf-8
"""
created by SL on 14-4-4
"""
from nowdo.controls.crowd_source_task import CrowdSourceTaskTagRel
from nowdo.utils.db_migration import create_tables, drop_tables, clear_all_data

__author__ = 'SL'

tables = [
    CrowdSourceTaskTagRel
]


def upgrade():
    clear_all_data()
    create_tables(tables)


def downgrade():
    drop_tables(tables)


if __name__ == "__main__":
    # downgrade()
    upgrade()