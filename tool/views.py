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

@json_response
def get_proxy_config(request):
    ret = {'data': None, 'status': 0, 'message': None}
    if request.method != 'GET':
        ret['message'] = 'use GET method'
        return ret
    db_session = Session()
    try:
        proxy_servers = db_session.query(ProxyServerORM).filter(
            text("busy is not true \
                order by {} {} limit 100".format(
                    random.choice(['id','last_check_time',
                                   'fail_cot','location']),
                    random.choice(['desc',''])
            ))).all()
        proxy_server = random.choice(proxy_servers)
        ret['data'] = {
            'ip': proxy_server.ip,
            'port': proxy_server.port,
            'location': proxy_server.location,
            'proxy_type': proxy_server.type,
        }
        proxy_server.busy = True
        db_session.commit()
        ret['status'] = 1
    except Exception as e:
        ret['message'] = str(e)
        print(str(e))
    db_session.close()
    return ret

