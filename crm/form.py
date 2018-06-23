# -*- coding: utf-8 -*-
from django.forms import ModelForm
from crm import models

class CustomerForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        fields = "__all__"

    #django是通过“__new__”方法，找到ModelForm里面的每个字段的，然后循环出每个字段添加自定义样式
    def __new__(cls, *args, **kwargs):
        #cls.base_fields是一个元祖，里面是 所有的  【(字段名，字段的对象),(),()】
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            #添加属性
            filed_obj.widget.attrs.update({'class':'form-control'})

        return ModelForm.__new__(cls)