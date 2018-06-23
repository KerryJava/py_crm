# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from kingadmin import app_setup

# 程序已启动就自动执行
app_setup.kingadmin_auto_discover()

from kingadmin.sites import site
from common.sites import site as comm_site

print('site', site.enable_admins)
print('site', comm_site.enable_admins)
site = comm_site


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
            return redirect(request.GET.get('next', '/kingadmin/'))
        else:
            error_msg = '用户名或密码错误！'

    return render(request, 'kingadmin/login.html', {'error_msg': error_msg})


def acc_logout(request):
    logout(request)
    return redirect("/login/")


def app_index(request):
    return render(request, 'kingadmin/app_index.html', {'site': site})


@login_required
def table_obj_list(request, app_name, model_name):
    '''取出指定model里的数据返回给前端'''
    # 拿到admin_class后，通过它找到拿到model
    admin_class = site.enable_admins[app_name][model_name]
    print("class ", admin_class)
    print("model", admin_class.model)
    querysets = admin_class.model.objects.all()
    print(querysets)
    querysets,filter_conditions = get_filter_result(request,querysets)
    admin_class.filter_conditions = filter_conditions

      #分页
    paginator = Paginator(querysets, 2)
    page = request.GET.get('page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)

    return render(request, 'kingadmin/table_obj_list.html', {'querysets': querysets, "admin_class":admin_class})


def get_filter_result(request,querysets):
    filter_conditions = {}
    #获取过滤的字段
    for key,val in request.GET.items():
        if key == 'page': continue
        if val:
            filter_conditions[key] = val
    #返回过滤后的数据
    return querysets.filter(**filter_conditions),filter_conditions
