# coding=utf8
import json
import traceback
# 暂时不要删除下面这一行!!!
from kfile.translation import msg_types as MsgCode
import sqlalchemy as SA
from sqlalchemy.dialects.mysql import BIGINT
from nowdo.controls.base import Base, id_generate
from nowdo.utils.nowdo_logger import nowdo_logger as logger



class Msg(Base):
    __tablename__ = 'msg'

    __DICT_ATTRS__ = ['id', 'type', 'msg', 'created_date']

    PER_PAGE = 30

    id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    type = SA.Column(SA.String(64), nullable=False)
    sender = SA.Column(SA.String(128), nullable=False)
    receiver = SA.Column(SA.String(128), nullable=False)
    msg = SA.Column(SA.String(512))

    def to_dict(self):
        res = {}
        for attr in Msg.__DICT_ATTRS__:
            res.update({attr: unicode(getattr(self, attr))})
        res.update(msg=json.loads(self.msg))
        return res #json.dumps(res)


class SRType:
    #发送者和接受者的类型
    SERVICE = 'SERVICE'
    SYSTEM = 'SYSTEM'
    USER = 'USER'


def srContact(type, sr):
    #连接发送者/接受者类型和发送者/接受者
    return type + ':' + sr


def msg2db(session, msg_type, sender_type, sender, receiver_type, receiver, **kwargs):
    try:
        for k, v in kwargs.items():
            if type(v) == str and len(v) > 100:
#                kwargs[k] = v[0:50] + '...'
                kwargs[k] = "..." + v[-len(v)/2:]
            if type(v) == unicode and len(v) > 40:
#                kwargs[k] = v[0:20] + '...'
                kwargs[k] = "..." + v[-len(v)/2:]
            if type(v) == list:
                if len(v) > 2:
                    v = [v[0]] + ["..."] + [v[-1]]
                for index, elem in enumerate(v):
                    if len(elem) > 40:
                        v[index] = "..." + elem[-len(elem)/2:]
                kwargs[k] = v

        msg_str = json.dumps(kwargs)
        if len(msg_str) > 512:
            logger.warn("Length Limit Exceeded! msg: %s" % msg_str)
            return

        msg = Msg(type=msg_type.get_code(), sender=srContact(sender_type, sender),
                  receiver=srContact(receiver_type, receiver), msg=msg_str)
        session.add(msg)
    except Exception as e:
        logger.error(traceback.format_exc())
