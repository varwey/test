# coding=utf-8
"""
created by SL on 14-3-24
"""
from sqlalchemy.orm import joinedload
from nowdo.controls.crowd_source_task import CrowdSourceTask
from nowdo.controls.group import Group
from nowdo.controls.topic import Topic, TopicComment
from nowdo.controls.account import Account
from nowdo.utils.escape_utils import strip_tags
from nowdo.utils.session import session_cm
from nowdo.utils.trends_utils import TREND_TARGET_TYPE_GROUP, TREND_TARGET_TYPE_TOPIC, TARGET_TYPE_MAP, TREND_TARGET_TYPE_TASK, TREND_TARGET_TYPE_COMMENT

__author__ = 'SL'


def _classify_target_ids(target_ids):
    """
    参数：Trends目标的id，可能是group.id， task.id, comment.id .etc
    返回：
        {
            'group': [group.id, ....],
            'task': [task.id, ....],
            'comment': [comment.id, ....]
            ...
        }
    """
    type_list = TARGET_TYPE_MAP.keys()
    target_type_id_list_map = {}

    def mapper(target_id_tuple):
        target_type, target_id = target_id_tuple
        for t in type_list:
            if target_type == t:
                if target_type in target_type_id_list_map:
                    target_type_id_list_map[target_type].append(target_id)
                else:
                    target_type_id_list_map[target_type] = [target_id]
    map(mapper, target_ids)
    return target_type_id_list_map


def _classify_target(db_session, target_type_id_list_map):
    """
    参数： _classify_target_ids 函数的返回值
    返回：
        {
            'group': { group.id: group, .....}
            'task': { task.id: task, .....}
            'topic': { topic.id: topic, .....}
            ...
        }
    """
    target_type_map = {}
    target_user_ids = []

    group_target_ids = target_type_id_list_map.get(TREND_TARGET_TYPE_GROUP)
    topic_target_ids = target_type_id_list_map.get(TREND_TARGET_TYPE_TOPIC)
    task_target_ids = target_type_id_list_map.get(TREND_TARGET_TYPE_TASK)
    comment_target_ids = target_type_id_list_map.get(TREND_TARGET_TYPE_COMMENT)

    if group_target_ids:
        group_list = db_session.query(Group).options(joinedload(Group.tags))\
            .filter(Group.id.in_(group_target_ids)).all()

        group_id_map = {}
        for t in group_list:
            target_user_ids.append(t.creator_id)
            group_id_map[t.id] = t

        target_type_map[TREND_TARGET_TYPE_GROUP] = group_id_map

    if topic_target_ids:
        topic_list = db_session.query(Topic) \
            .filter(Topic.id.in_(topic_target_ids)) \
            .options(joinedload(Topic.comments)) \
            .all()

        topic_id_map = {}
        for t in topic_list:
            topic_id_map[t.id] = t
            target_user_ids.append(t.creator_id)

        target_type_map[TREND_TARGET_TYPE_TOPIC] = topic_id_map

    if task_target_ids:
        task_list = db_session.query(CrowdSourceTask) \
            .filter(CrowdSourceTask.id.in_(task_target_ids)).all()

        task_id_map = {}
        for t in task_list:
            target_user_ids.append(t.creator_id)
            task_id_map[t.id] = t

        target_type_map[TREND_TARGET_TYPE_TASK] = task_id_map

    if comment_target_ids:
        comment_list = db_session.query(TopicComment) \
            .filter(TopicComment.id.in_(comment_target_ids)).all()

        comment_id_map = {}
        for t in comment_list:
            target_user_ids.append(t.creator_id)
            comment_id_map[t.id] = t

        target_type_map[TREND_TARGET_TYPE_COMMENT] = comment_id_map

    return target_type_map, target_user_ids


class FormattedTrends(object):
    """
        格式化后的动态
    """
    def __init__(self, target, user, target_user, action, action_str, target_type, target_title,
                 target_content, expand, target_url, action_date):
        self.user = user
        self.target_user = target_user
        self.target = target
        self.action = action
        self.action_str = action_str
        self.target_title = target_title  # 如：group, topic .etc
        self.target_content = target_content
        self.target_url = target_url
        self.target_type = target_type  # 如：Group, Topic
        self.action_date = action_date
        self.expand = expand

    @staticmethod
    def get_formatted_trends_list(object_list):
        if not object_list:
            return []
        user_ids = [t.user_id for t in object_list]
        with session_cm() as db_session:

            target_ids = [(t.target_type, t.target_id) for t in object_list]
            target_type_id_list_map = _classify_target_ids(target_ids)

            target_type_map, target_user_ids = _classify_target(db_session, target_type_id_list_map)

            user_ids.extend(target_user_ids)
            user_ids_distinct = list(set(user_ids))

            user_list = db_session.query(Account).filter(Account.id.in_(user_ids_distinct))
            user_id_map = dict([(u.id, u) for u in user_list])

            trends_list = []
            for trends in object_list:

                target = target_type_map[trends.target_type].get(trends.target_id)
                formatted_trends = FormattedTrends(user=user_id_map.get(trends.user_id),
                                                   target_user=user_id_map.get(target.creator_id),
                                                   target=target,
                                                   action=trends.action,
                                                   action_str=trends.action_str,
                                                   target_type=trends.target_type,
                                                   target_url=trends.target_url,
                                                   target_title=trends.target_title(target),
                                                   target_content=trends.target_content(target),
                                                   expand=(len(strip_tags(trends.target_content(target))) > 300),
                                                   action_date=trends.created_date)
                trends_list.append(formatted_trends)
            return trends_list