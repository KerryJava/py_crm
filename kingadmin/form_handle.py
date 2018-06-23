# -*- coding: utf-8 -*-
# kingadmin/formhandle.py

from django.forms import ModelForm


def create_dynamic_model_form(admin_class):
    '''动态生成modelform'''

    class Meta:
        model = admin_class.model
        fields = "__all__"
        name = admin_class.model.__str__

    def __str__():
        return admin_class.model.__str__

    def my_name(self):
        return admin_class.model

    # 动态生成ModelForm
    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, "my_name": my_name})

    return dynamic_form
