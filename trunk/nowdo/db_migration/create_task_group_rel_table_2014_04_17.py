# coding=utf-8
"""
created by SL on 14-4-15
"""
from sqlalchemy.dialects.mysql.base import BIGINT
from nowdo.controls.group import GroupTaskRelTable
from nowdo.controls.like import LikeRel
from nowdo.utils.db_migration import create_tables, drop_tables, clear_all_data, drop_foreign_key, drop_column, create_column
import sqlalchemy as SA

__author__ = 'SL'

tables = [
    GroupTaskRelTable,
    LikeRel
]

creator_col = SA.Column("creator", SA.String(64), index=True, nullable=True)

creator_id_col = SA.Column("creator_id", BIGINT(unsigned=True), index=True, nullable=False)


def upgrade():
    drop_foreign_key("crowd_source_task", "group", "group_id", "id")
    clear_all_data()
    create_tables(tables)
    drop_column('crowd_source_task', creator_col)
    create_column('crowd_source_task', creator_id_col, index_name="creator_id")


def downgrade():
    drop_tables(tables)
    create_column('crowd_source_task', creator_col, index_name="creator")
    drop_column('crowd_source_task', creator_id_col)


if __name__ == "__main__":
    # downgrade()
    upgrade()
