# -*- coding: utf-8 -*-
from nowdo.controls.account import Account
from nowdo.controls.crowd_source_task import CrowdSourceTaskComment
from nowdo.controls.notice import Notice

__author__ = 'lhfu'


class FormattedNotice(object):
    """
        格式化后的动态
    """
    def __init__(self, sender, receiver, type, target, is_read, created_date):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.created_date = created_date
        self.target = target
        self.is_read = is_read

    @classmethod
    def _classify_target_ids(cls, target_ids):
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
        target_type_id_list_map = {}

        def mapper(target_id_tuple):
            target_type, target_id = target_id_tuple
            for t in Notice.type_list:
                if target_type == t:
                    if target_type in target_type_id_list_map:
                        target_type_id_list_map[target_type].append(target_id)
                    else:
                        target_type_id_list_map[target_type] = [target_id]
        map(mapper, target_ids)
        return target_type_id_list_map

    @classmethod
    def _classify_target(cls, db_session, target_type_id_list_map):
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

        follow_target_ids = target_type_id_list_map.get(Notice.NOTICE_TYPE_FOLLOW)
        comment_target_ids = target_type_id_list_map.get(Notice.NOTICE_TYPE_COMMENT)

        if follow_target_ids:
            target_type_map[Notice.NOTICE_TYPE_FOLLOW] = {}

        if comment_target_ids:
            comment_list = db_session.query(CrowdSourceTaskComment) \
                .filter(CrowdSourceTaskComment.id.in_(comment_target_ids)).all()

            comment_id_map = {}
            for t in comment_list:
                comment_id_map[t.id] = t

            target_type_map[Notice.NOTICE_TYPE_COMMENT] = comment_id_map

        return target_type_map

    @classmethod
    def get_notices_by_receiver(cls, db_session, receiver_id, page=None, per_page=None):
        notice_pagination = Notice.get_notice_list(db_session, receiver_id, page=page, per_page=per_page)
        print notice_pagination
        if not notice_pagination:
            return []
        object_list = notice_pagination.object_list
        print object_list

        target_ids = [(t.type, t.related_event_id) for t in object_list]

        target_type_id_list_map = cls._classify_target_ids(target_ids)

        target_type_map = cls._classify_target(db_session, target_type_id_list_map)

        user_id_list = []
        for notice in object_list:
            user_id_list.append(notice.receiver_id)
            user_id_list.append(notice.sender_id)

        user_id_list = list(set(user_id_list))

        user_list = db_session.query(Account).filter(Account.id.in_(user_id_list)).all()
        user_id_map = dict([(u.id, u) for u in user_list])

        notice_list = []
        for notice in object_list:
            target = target_type_map[notice.type].get(notice.related_event_id)
            formatted_notice = cls(
                sender=user_id_map[notice.sender_id],
                receiver=user_id_map[notice.receiver_id],
                type=notice.type,
                created_date=notice.created_date,
                target=target,
                is_read=notice.is_read,
            )
            notice_list.append(formatted_notice)
            notice.is_read = True
        db_session.commit()

        return notice_list