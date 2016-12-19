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
from django_rq import job

@job('high')
def free_back_proxy_item(proxy_server):
    print('free back')
    return 1



