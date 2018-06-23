# -*- coding: utf-8 -*-
# kingadmin/formhandle.py

from django.forms import ModelForm


def create_dynamic_model_form(admin_class, form_add=False):
    '''动态生成modelform'''

    class Meta:
        model = admin_class.model
        fields = "__all__"
        name = admin_class.model.__str__
        exclude = admin_class.readonly_fields

        if not form_add:
            exclude = admin_class.readonly_fields
            admin_class.form_add = False
        else:
            admin_class.form_add = True

    # django是通过“__new__”方法，找到ModelForm里面的每个字段的，然后循环出每个字段添加自定义样式

    def __new__(cls, *args, **kwargs):
        # cls.base_fields是一个元祖，里面是 所有的  【(字段名，字段的对象),(),()】
        for field_name in cls.base_fields:
            # 每个字段的对象
            filed_obj = cls.base_fields[field_name]
            # 添加属性
            filed_obj.widget.attrs.update({'class': 'form-control'})

        return ModelForm.__new__(cls)

    def __str__():
        return admin_class.model.__str__

    def my_name(self):
        return admin_class.model

    # 动态生成ModelForm
    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, "my_name": my_name, '__new__': __new__})

    return dynamic_form
