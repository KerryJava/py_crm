# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
__author__ = 'derek'

from django.db import models
from django.contrib.auth.models import User

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=64, unique=True)  # 不能重
    # 一个角色可以访问多个菜单，一个菜单可以被多个角色访问
    menus = models.ManyToManyField('Menus', blank=True, verbose_name='动态菜单')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    '''用户信息表'''
    # 关联django自带的User，可以自己扩展字段
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('姓名', max_length=64)
    # 一个用户可以有多个角色，一个角色可以对应多个用户
    role = models.ManyToManyField(Role, blank=True, null=True)

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    '''客户信息表'''
    name = models.CharField('姓名', max_length=64, default=None)
    contact_type_choices = ((0, 'qq'), (1, '微信'), (2, '手机'))
    contact_type = models.SmallIntegerField(choices=contact_type_choices, default=0)
    contact = models.CharField('联系方式', max_length=64, unique=True)
    source_choices = ((0, 'qq群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其它'),)
    source = models.SmallIntegerField('客户来源', choices=source_choices)
    # 关联自己，如果是转介绍（介绍人已经是学员，然后介绍别人过来学习），需要填写转介绍人的信息，不是转介绍，这里就可以为空
    referral_from = models.ForeignKey('self', blank=True, null=True, verbose_name='转介绍', on_delete=models.CASCADE)
    # 可以咨询多个课程
    consult_courses = models.ManyToManyField('Course', verbose_name='咨询课程')
    consult_content = models.TextField('咨询内容', )
    status_choices = ((0, '未报名'), (1, '已报名'), (2, '已经退学'))
    status = models.SmallIntegerField('客户状态', choices=status_choices, default=0)
    consultant = models.ForeignKey('UserProfile', verbose_name='课程顾问', on_delete=models.CASCADE)
    date = models.DateField('创建的时间', auto_now_add=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    '''学员表'''
    customer = models.ForeignKey('CustomerInfo', verbose_name='客户', on_delete=models.CASCADE)
    class_grades = models.ForeignKey('ClassList', verbose_name='班级', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.customer.__str__()


class CustomerFollowUp(models.Model):
    '''客户跟踪记录表'''
    customer = models.ForeignKey('CustomerInfo', on_delete=models.CASCADE)
    content = models.TextField('跟踪内容', )
    user = models.ForeignKey('UserProfile', verbose_name='跟进人', on_delete=models.CASCADE)
    status_choices = ((0, '近期无报名计划'), (1, '一个月内报名'), (2, '半个月报名'), (3, '已报名'),)
    status = models.SmallIntegerField('客户状态', choices=status_choices)
    date = models.DateField('创建的时间', auto_now_add=True)


class Course(models.Model):
    '''课程表'''
    name = models.CharField('课程名称', max_length=64, unique=True)
    # 价格必须为整数
    price = models.PositiveSmallIntegerField('价格', )
    period = models.PositiveSmallIntegerField('课程周期（月）', default=5)
    outline = models.TextField('大纲', )

    def __str__(self):
        return self.name


class ClassList(models.Model):
    '''班级列表'''
    branch = models.ForeignKey('Branch', verbose_name='校区', on_delete=models.CASCADE)
    # 一个班级只能有一个课程，一个课程可以有多个班级
    course = models.ForeignKey('Course', verbose_name='课程', on_delete=models.CASCADE)
    class_type_choices = ((0, '脱产'), (1, '周末'), (2, '网络班'))
    class_type = models.SmallIntegerField('班级类型', choices=class_type_choices, default=0)
    semester = models.SmallIntegerField(u'semester', default=1)
    teachers = models.ManyToManyField('UserProfile', verbose_name='讲师')
    start_date = models.DateField('开班日期', )
    # 毕业日期因为不固定，所以可以为空
    graduate_date = models.DateField('毕业日期', blank=True, null=True)

    def __str__(self):
        # 班级名是课程名+第几期拼接起来的
        str = "%s(%d) %s" % (self.course.name, self.semester, u"学期")
        return str.encode("utf-8")

    class Meta:
        # 联合唯一，班级不能重复
        unique_together = ('branch', 'class_type', 'course', 'semester')


class CourseRecord(models.Model):
    '''上课记录'''
    class_grade = models.ForeignKey('ClassList', verbose_name='上课班级', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField('课程节次', )
    teacher = models.ForeignKey('UserProfile', verbose_name='讲师', on_delete=models.CASCADE)
    title = models.CharField('本节主题', max_length=64)
    content = models.TextField('本节内容', )
    has_homework = models.BooleanField('本节有作业', default=True)
    homework = models.TextField('作业需求', blank=True, null=True)
    date = models.DateField('创建的时间', auto_now_add=True)

    def __str__(self):
        # 上课班级+课程节次
        name = "%s第(%d)节" % (self.class_grade, self.day_num)
        return name.encode('utf-8')

    class Meta:
        unique_together = ('class_grade', 'day_num')


class StudyRecord(models.Model):
    '''学习记录表'''
    # 一节课对应多个学生
    course_record = models.ForeignKey('CourseRecord', verbose_name='课程', on_delete=models.CASCADE)
    # 一个学生有多个上课记录
    student = models.ForeignKey('Student', verbose_name='学生', on_delete=models.CASCADE)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (75, 'B-'),
                     (70, 'C+'),
                     (60, 'C'),
                     (40, 'C-'),
                     (-50, 'D'),
                     (0, 'N/A'),  # not avaliable
                     (-100, 'COPY'),  # 抄作业
                     )
    score = models.SmallIntegerField('得分', choices=score_choices, default=0)
    show_choices = ((0, '缺勤'),
                    (1, '已签到'),
                    (2, '迟到'),
                    (3, '早退'),
                    )
    show_status = models.SmallIntegerField('出勤', choices=show_choices, default=1)
    note = models.TextField('成绩备注', blank=True, null=True)
    date = models.DateField('创建的时间', auto_now_add=True)

    def __str__(self):
        name = "%s %s %s" % (self.course_record, self.student, self.score)
        return name.encode('utf-8')


class Branch(models.Model):
    '''校区分支'''
    name = models.CharField('校区名', max_length=64, unique=True)
    addr = models.CharField('地址', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class Menus(models.Model):
    '''动态菜单'''
    name = models.CharField(max_length=64)
    # 绝对url和动态url
    url_type_choices = ((0, 'absolute'), (1, 'dynamic'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url_name')
