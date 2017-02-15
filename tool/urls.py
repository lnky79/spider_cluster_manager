#coding:utf-8
"""
@file:      urls
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-12-18 17:34
@description:
            url config of "tool" app
"""

from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^get_proxy_configs$',get_proxy_configs),
    url(r'^free_server$',free_server),
    ]
