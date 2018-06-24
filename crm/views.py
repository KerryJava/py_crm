# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import IntegrityError
from django.shortcuts import render
# Create your views here.
import sys
import os
import json

sys.path.append("..")
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django import conf
from django.utils.timezone import datetime
from django import forms
from .models import UserProfile, Role, Menus
from crm import models
from crm import form


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

    profile_list = UserProfile.objects.filter(email=user.email)
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


@login_required
def stu_enrollment(request):
    customers = models.CustomerInfo.objects.all()
    class_lists = models.ClassList.objects.all()

    if request.method == 'POST':
        # 获取提交的客户id和班级id，然后生成报名链接
        customer_id = request.POST.get('customer_id')
        class_grade_id = request.POST.get('class_grade_id')
        user = request.user
        profile = UserProfile.objects.filter(user=user).first()
        profile_id = profile.id
        try:
            enrollment_obj = models.StudentEnrollment.objects.create(
                customer_id=customer_id,
                class_grade_id=class_grade_id,
                consultant_id=profile_id
            )
        # 已经生成过报名链接，就进入审核页面
        except IntegrityError as e:
            print("already enroll")
            enrollment_obj = models.StudentEnrollment.objects.get(customer_id=customer_id,
                                                                  class_grade_id=class_grade_id)
            if enrollment_obj.contract_agreed:
                return redirect("/crm/stu_enrollment/%s/contract_audit/" % enrollment_obj.id)
        # 生成链接返回到前端
        enrollment_link = "http://localhost:8000/crm/enrollment/%s" % enrollment_obj.id

    return render(request, 'crm/stu_enrollment.html', locals())


def enrollment(request, enrollment_id):
    '''学员在线报名表地址'''

    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)

    if request.method == 'POST':
        customer_form = form.CustomerForm(instance=enrollment_obj.customer, data=request.POST)
        if customer_form.is_valid():
            customer_form.save()
            enrollment_obj.contract_agreed = True
            enrollment_obj.contract_signed_date = datetime.now()
            enrollment_obj.save()
            print(enrollment_obj.contract_agreed)
            print("enrollment obj")
            return HttpResponse("你已成功提交报名信息，请等待审核，欢迎加入仙剑奇侠传")
    else:
        customer_form = form.CustomerForm(instance=enrollment_obj.customer)

    return render(request, 'crm/enrollment.html', locals())


@csrf_exempt
def enrollment_fileupload(request, enrollment_id):
    '''学员报名文件上传'''
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UOLOAD_DIR, enrollment_id)
    # 第一次上传图片就创建目录，学员上传第二章图片的时候，会判断目录是否已经存在
    # 因为如果目录存在还mkdir就会报错，所以这里要做判断
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)
    # 获取上传文件的对象
    file_obj = request.FILES.get('file')
    # 最多只允许上传3个文件
    if len(os.listdir(enrollment_upload_dir)) <= 3:
        # 把图片名字拼接起来（file.name：上传的文件名字）
        with open(os.path.join(enrollment_upload_dir, file_obj.name), 'wb') as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        return HttpResponse(json.dumps({'status': False, 'err_msg': '最多只能上传三个文件'}))

    return HttpResponse(json.dumps({'status': True, }), )


@login_required
def contract_audit(request, enrollment_id):
    '''合同审核'''

    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    if request.method == 'POST':
        enrollment_form = form.EnrollmentForm(instance=enrollment_obj, data=request.POST)
        if enrollment_form.is_valid():
            enrollment_form.save()
            stu_obj = models.Student.objects.get_or_create(customer=enrollment_obj.customer)[0]
            # m2m, 添加班级
            # stu_obj.class_grades.add(enrollment_obj.class_grade_id)
            print("audit")
            print (enrollment_obj.class_grade)
            print (enrollment_obj.class_grade.student_set)
            print (stu_obj.class_grades)
            enrollment_obj.class_grade.student_set.add(stu_obj)
            # stu_obj.save()
            # 改变报名
            enrollment_obj.customer.status = 1
            enrollment_obj.consultant_approved_date = datetime.now()
            enrollment_obj.save()
            return redirect("/kingadmin/crm/customerinfo/%s/change" % enrollment_obj.customer.id)
    else:
        # 拿到客户信息的表单
        customer_form = form.CustomerForm(instance=enrollment_obj.customer)
        enrollment_form = form.EnrollmentForm(instance=enrollment_obj)
    return render(request, 'crm/contract_audit.html', locals())
