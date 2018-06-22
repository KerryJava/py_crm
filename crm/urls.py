# -*- coding: utf-8 -*-
# crm/urls.py

from django.conf.urls import url, include
from crm import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^logout/', views.acc_logout,name='logout'),
    url(r'^login/', views.acc_login, name='login'),
    url(r'^test/', views.acc_login, name='logint')
]