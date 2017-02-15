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
import time

def free_back_proxy_item(ip,wait_seconds=0):
    db_session = Session()
    try:
        proxy_server = db_session\
            .query(ProxyServerORM).filter_by(ip=ip)[0]
    except IndexError:
        err = 'No such ip in database : {}'.format(ip)
        print(err)
        raise IndexError(err)
    proxy_server.busy = False
    print('free ip: {} after {} seconds...'\
          .format(proxy_server.ip,wait_seconds))
    time.sleep(wait_seconds)
    try:
        db_session.commit()
        res = True
        print('free ip: {} success!'\
              .format(proxy_server.ip))
    except Exception as e:
        print('free ip: {} failed: {}'\
              .format(proxy_server,ip,str(e)))
        res = False
    db_session.close()
    return res
