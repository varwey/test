# coding=utf-8
"""
created by SL on 14-4-15
"""
from nowdo.controls.crowd_source_task import CrowdSourceTaskContent
from nowdo.utils.db_migration import create_tables, drop_tables, alter_column

__author__ = 'SL'

tables = [
    CrowdSourceTaskContent
]


def upgrade():
    create_tables(tables)
    alter_column('crowd_source_task', 'file_id', nullable=True)


def downgrade():
    drop_tables(tables)
    alter_column('crowd_source_task', 'file_id', nullable=False)


if __name__ == "__main__":
    downgrade()
    upgrade()
