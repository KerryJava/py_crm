# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django import conf
from kingadmin import sites

def kingadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            # 去每个app下面执行kingadmin.py文件
            mod = __import__('%s.kingadmin' % app_name)
            print("kingadmin import module  mod %s", mod.kingadmin)
            # 打印每个app已注册的model名字
            # print(mod)
            # print("success")
            method_to_call = getattr(mod.kingadmin, 'get_admin_and_model')
            admin , models = method_to_call()
            for model in models:
                sites.site.register(model, admin)
            pass
        except ImportError as e:
            print e
            print("kingadmin import module error  mod ", app_name, ('%s.kingadmin' % app_name))
            pass