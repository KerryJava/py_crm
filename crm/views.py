# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
# Create your views here.
import sys
sys.path.append("..")
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UserProfile, Role, Menus
# from kingadmin import app_setup

# 程序一启动就自动执行
# app_setupup.kingadmin_auto_discover()


def acc_login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # user是一个对象
        # 验证
        user = authenticate(username=username, password=password)
        if user:
            # 登录（已生成session）
            login(request, user)
            # 如果有next值就获取next值，没有就跳转到首页
            return redirect(request.GET.get('next', settings.HOME_PAGE))
        else:
            error_msg = '用户名或密码错误！'

    return render(request, 'login.html', {'error_msg': error_msg, 'app_title': "mojicai system"})


@login_required
def dashboard(request):
    user = request.user

    print(user)
    print(type(user))
    print(user.username)
    print(user.id)

    menus = []

    profile_list = UserProfile.objects.filter(user=user)
    for profile_item in profile_list:
        print(profile_item.name)
        print(type(profile_item))
        print(type(profile_item.role))
        print(profile_item.role.all())
        roles = profile_item.role.all()

        for role in roles:
            print (role.menus.all())
            menus = menus + list(role.menus.all())

    return render(request, 'crm/dashboard.html', locals())


def acc_logout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)
