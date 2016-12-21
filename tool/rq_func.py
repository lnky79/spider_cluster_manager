#coding:utf-8
"""
@file:      rq_func.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm Mac
@create:    2016/12/19 16:32
@description:
            存放异步周期任务，与rq task queue相关
"""
from db_config import Session
from .models import ProxyServerORM

def free_back_proxy_item(proxy_server=None,ip=None):
    db_session = Session()
    if ip and proxy_server is None:
        proxy_server = db_session\
            .query(ProxyServerORM)\
            .filter_by(ip=ip)[0]
    proxy_server.busy = False
    print('free ip: {}'.format(proxy_server.ip))
    try:
        db_session.commit()
        res = True
    except Exception as e:
        print(str(e))
        res = False
    db_session.close()
    return res
