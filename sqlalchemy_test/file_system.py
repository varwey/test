#/usr/bin/env python2.7
#coding:utf8

"""
One simple test of sqlalchemy
2014/06/18 by varwey
"""

from sqlalchemy import *
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///data.db')
Base = declarative_base()

"""
metadata = MetaData('sqlite:///data.db')
user_table = Table(
    'tf_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', Unicode(16),
           unique=True, nullable=False),
    Column('password', Unicode(40), nullable=False),
    Column('display_name', Unicode(255), default=''),
    Column('created', DateTime, default=datetime.now()),)
"""

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    addresses = relationship('Address', backref='user', cascade='all, delete, delete-orphan')

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.fullname, self.name)

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    #user = relationship('User', backref=backref('addresses', order_by=id))

    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return "<Address('%s')>" % self.email_address

post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('keyword_id', Integer, ForeignKey('keywords.id'))
)

class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    keywords = relationship('Keyword', secondary=post_keywords, backref='posts')

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)

    def __init__(self, keyword):
        self.keyword = keyword

    def __repr__(self):
        return "<Keyword('%s')>" % (self.keyword, )

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

BlogPost.author = relationship(User, backref=backref('posts', lazy='dynamic'))
Base.metadata.create_all(engine)

print '>>> User.__table__\n%s'%User.__table__

t_user = User('tt', 'Tt jim', 'ttpassword')
print '>>> t_user.name\n%s'%t_user.name
print '>>> t_user.password\n%s'%t_user.password

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

t_user = User('weiwei', 'Tt jim', 'ttpassword')
session.add(t_user)
#session.commit()

print """
>>> for row in session.query(User).filter(User.name=='tt').all()\n
>>>     print 'name: %s\\npassword%s' % (row.name, row.password)\n
      """
for row in session.query(User).filter(User.name=='tt').all():
    print 'name: %s\npassword: %s' % (row.name, row.password)

print session.query(User).filter(User.name=='tt').first()

try:
    #print session.query(User).filter(User.name=='tt').one()
    print session.query(User).filter(User.id==1).one()
except Exception, e:
    print 'raise a except: %s'%e

"""
session.add_all([
    User('guanguang', 'pang', 'pppppp'),
    Apple('108g', 'bule', 'hebei'),
    User('xixi', 'xxxx', 'iiiii')])

session.commit()

print session.query(User).all()
print session.query(Apple).all()
"""

#别名,过滤,排序,换行
for row in session.query(User.name.label('user_name')).\
          filter_by(name='weiwei').order_by('-id'):
    print row.user_name

user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all():
    print row.user_alias

q = session.query(User.id, User.name)
print q.order_by('name').all()

ua = aliased(User)
qq = q.from_self(User.id, User.name, ua.name).\
     filter(User.name < ua.name).\
     filter(func.length(ua.name) != func.length(User.name))
print qq.order_by('name').all()

weiwei = session.query(User).filter_by(id=1).one()
#print weiwei.addresses
print weiwei.addresses#, weiwei.addresses[1].user

"""
weiwei.addresses = [
                    Address(email_address='varwey.py@gmail.com'),
                    Address(email_address='13241848354@163.com'),
                    Address(email_address='857773753@qq.com')]

print weiwei.addresses, weiwei.addresses[1].user

session.add(weiwei)
session.commit()
"""

weiwei = session.query(User).filter_by(name='weiwei').first()
print 'weiwei: %s'%weiwei
print 'weiwei.addresses: %s'%weiwei.addresses

for u, a in session.query(User, Address).\
                    filter(User.id==Address.user_id).\
                    filter(Address.email_address.in_([
                                                     'varwey.py@gmail.com',
                                                     'jack@yahoo.com'])).\
                    all():
    print u, a

stmt = exists().where(Address.user_id==User.id)
for name, in session.query(User.name).filter(stmt):
    print 'name: %s'%name

for name, in session.query(User.name).\
                     filter(User.addresses.any()):
    print 'any name: %s'%name

jack = session.query(User).get(1)
print 'jack: %s'%jack

del jack.addresses[1]
addr = session.query(Address).filter(Address.id==jack.id).count()
print addr

session.delete(jack)
addr = session.query(Address).filter(Address.id==jack.id).count()
print 'end addr: %s'%addr

xixi = session.query(User).filter_by(name='xixi').one()
print 'xixi: %s'%xixi

post = BlogPost("Xixi is my girlfriend !!!", "This is really.", xixi)
session.add(post)
post.keywords.append(Keyword('xixi'))
post.keywords.append(Keyword('firstpost'))

print session.query(BlogPost).\
                  filter(BlogPost.keywords.any(keyword='firstpost')).\
                  all()
print session.query(BlogPost).\
                  filter(BlogPost.author==xixi).\
                  filter(BlogPost.keywords.any(keyword='xixi')).\
                  all()

print xixi.posts.filter(BlogPost.keywords.any(keyword='xixi')).all()

