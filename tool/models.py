#coding:utf-8
"""
@file:      models.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-12-18 16:04
@description:
            spider tools database ORM models
"""
from sqlalchemy import (
    Column, Integer,
    String, DateTime,Boolean,
)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class ProxyServerORM(Base):
    __tablename__ = 'proxy_server'

    id = Column(Integer,
        primary_key=True,autoincrement=True)
    ip = Column(String)
    port = Column(Integer)
    location = Column(String)
    is_anonymous = Column(Boolean)
    type = Column(String)
    type2 = Column(String)
    last_check_time = Column(DateTime)
    check_in_this_session = Column(Boolean)
    fail_cot = Column(Integer)
    busy = Column(Boolean)

    def __repr__(self):
        return (
            "<ProxyServerORM(ip={},port={},location={})>"
        ).format(self.ip,self.port,self.location)