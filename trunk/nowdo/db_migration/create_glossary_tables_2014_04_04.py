# coding=utf-8
"""
created by SL on 14-4-4
"""
from nowdo.controls.glossary import Glossary, GlossaryTable, CheckingGlossary, GlossaryTableTaskRelTable
from nowdo.utils.db_migration import create_tables, drop_tables

__author__ = 'SL'

tables = [
    Glossary,
    GlossaryTable,
    CheckingGlossary,
    GlossaryTableTaskRelTable
]


def upgrade():
    create_tables(tables)


def downgrade():
    drop_tables(tables)


if __name__ == "__main__":
    downgrade()
    # upgrade()