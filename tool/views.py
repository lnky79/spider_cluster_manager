#coding:utf-8
"""
@file:      views.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-12-18 15:44
@description:
            spider tools api views function
"""

from public_func import *
from .models import ProxyServerORM
from db_config import Session
from sqlalchemy import text
from .rq_func import *

from datetime import datetime,timedelta
import django_rq

@json_response
def free_server(request):
    ret = {'status': 0, 'err_msg': None}
    if request.method != 'GET':
        ret['err_msg'] = 'use GET method'
        return ret
    ip = request.GET['ip']
    try:
        free_back_proxy_item(ip=ip)
        ret['status'] = 1
    except Exception as e:
        ret['err_msg'] = str(e)
    return ret


@json_response
def get_proxy_config(request):
    ret = {'data': None, 'status': 0, 'message': None}
    if request.method != 'GET':
        ret['message'] = 'use GET method'
        return ret
    db_session = Session()
    try:
        proxy_servers = db_session.query(ProxyServerORM).filter(
            text(
                "busy is not true order \
                by fail_cot limit 10")
        ).all()
        proxy_server = random.choice(proxy_servers)
        ret['data'] = {
            'ip': proxy_server.ip,
            'port': proxy_server.port,
            'location': proxy_server.location,
            'proxy_type': proxy_server.type,
            'fail_cot': proxy_server.fail_cot
        }
        proxy_server.busy = True
        db_session.commit()
        print('get server: {}'.format(proxy_server))

        scheduler = django_rq.get_scheduler('default')
        scheduler.enqueue_in(
            timedelta(seconds=1),
            free_back_proxy_item,
            proxy_server
        )

        django_rq.enqueue(free_back_proxy_item,
                        {'proxy_server': proxy_server})

        ret['status'] = 1
    except Exception as e:
        ret['message'] = str(e)
        print(str(e))
    db_session.close()
    return ret

