# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.utils.db_migration import get_table, create_column, drop_column


def upgrade():
    create_column('crowd_source_task',
                  Column('type', BIGINT(unsigned=True), nullable=True, default=CrowdSourceTask.TASK_TYPE_TEXT))


def downgrade():
    drop_column('crowd_source_task', Column('type', BIGINT(unsigned=True), nullable=True))


if __name__ == '__main__':
    #downgrade()
    upgrade()