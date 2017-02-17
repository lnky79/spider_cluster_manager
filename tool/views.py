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

def basic_req_for_proxy(quantity=0,get_all_valid=1,
        is_anonymous=True):
    db_session = Session()
    servers = []
    try:
        if get_all_valid:
            proxy_servers=db_session.query(ProxyServerORM)\
                .filter(ProxyServerORM.fail_cot < 0)
        else:
            pass
        if is_anonymous:
            proxy_servers = proxy_servers.filter(\
                ProxyServerORM.is_anonymous==True).all()
        '''
        scheduler = django_rq.get_scheduler('default')
        scheduler.enqueue_in(
            timedelta(seconds=1),
            free_back_proxy_item,
            proxy_server
        )
        django_rq.enqueue(free_back_proxy_item,
                        {'proxy_server': proxy_server})
        '''
        servers =  [ proxy_server.to_dict() for proxy_server in proxy_servers]
    except Exception as e:
        print(str(e))
    db_session.close()
    return servers

@json_response
def get_proxy_configs(request):
    ret = {'data': None, 'status': 0, 'message': None}
    if request.method != 'GET':
        ret['message'] = 'use GET method'
        return ret
    default_dict = {
        'quantity': 0,
        'get_all_valid': 1,
        'is_anonymous': 0,
    }
    for key in default_dict.keys():
        if key in request.GET.keys():
            default_dict[key] = int(request.GET[key])
    ret['data'] = basic_req_for_proxy(**default_dict)
    print(ret['data'])
    ret['status'] = 1
    return ret

