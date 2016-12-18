#coding:utf-8
"""
@file:      public_func.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-12-18 15:44
@description:
            public function for web service api
"""

import json,datetime,time,random

from django.http.response import HttpResponse

class Timer:
    def __init__(self):
        self.start_ok = False

    def start(self):
        self.st = time.time()
        self.start_ok = True

    def end(self):
        if not self.start_ok:
            raise Exception('[Error] in Timer: Please run start() first.')
        self.gap = round(time.time()-self.st,2)


class CJsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime( '%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime( "%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self,obj)


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        tm = Timer()
        tm.start()
        objects = func(request, *args, **kwargs)
        tm.end()
        print('Response time: {} s\n'.format(tm.gap))
        if isinstance(objects, HttpResponse):
            return object#服务端不希望返回jsonp的情况
        try:
            data = json.dumps(objects,cls=CJsonEncoder)
            if 'callback' in request.GET or 'callback' in request.POST:
                #给跨域的jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except Exception as e:
            #服务端希望返回jsonp，但因为故障，不得不妥协成传string
            print('json_response error:',str(e))
            object['status'] = 2
            object['message'] = 'json_response() error, your got one string type'
            data = json.dumps(str(objects))
        return HttpResponse(data)#这里是返回给我的环境
    return decorator

from datetime import datetime, timedelta, timezone
def get_beijing_time(format='%Y-%m-%d %H:%M:%S'):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(timezone(timedelta(hours=8))) \
        .strftime(format)


def try_int(val):
    try:
        return int(val)
    except:
        return val
