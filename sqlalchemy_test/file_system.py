#/usr/bin/env python2.7
#coding:utf8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

class Apple(Base):
    __tablename__ = 'apples'

    id = Column(Integer, Sequence('apple_id_seq'), primary_key=True)
    weight = Column(String(50))
    color = Column(String(50))
    attribution = Column(String(20))

    def __init__(self, weight, color, attribution):
        self.weight = weight
        self.color = color
        self.attribution = attribution

    def __repr__(self):
        return "<Apple('%s', '%s', '%s')>" % (self.weight, self.color, self.attribution)

Base.metadata.create_all(engine)

