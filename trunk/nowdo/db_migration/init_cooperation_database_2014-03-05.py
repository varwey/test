# coding=utf-8
"""
created by SL on 14-3-5
"""
from nowdo.controls.entry import Entry
from nowdo.controls.file import File
from nowdo.controls.file_content import FileContent
from nowdo.controls.follows import Follow
from nowdo.controls.group import Group, GroupUserRel, GroupTagRelTable
from nowdo.controls.crowd_source_task import CrowdSourceTask, CrowdSourceTaskParticipator, \
    CrowdSourceTaskResult, CrowdSourceTaskResultVote
from nowdo.controls.group_property import GroupProperty
from nowdo.controls.mail import Mail, Dialogue
from nowdo.controls.tag import Tag
from nowdo.controls.topic import Topic, TopicComment
from nowdo.controls.trends import Trends
from nowdo.utils.db_migration import create_tables, drop_tables

__author__ = 'SL'

tables = [
    Group,
    GroupProperty,
    GroupUserRel,
    CrowdSourceTask,
    CrowdSourceTaskParticipator,
    CrowdSourceTaskResult,
    CrowdSourceTaskResultVote,
    Topic,
    TopicComment,
    Entry,
    File,
    Trends,
    Tag,
    GroupTagRelTable,
    FileContent,
    Follow,
    Dialogue,
    Mail,
]


def upgrade():
    create_tables(tables)


def downgrade():
    after_delete_tables = [CrowdSourceTask, Group]
    drop_tables(set(tables)-set(after_delete_tables))
    drop_tables(after_delete_tables)


if __name__ == "__main__":
    # downgrade()
    upgrade()