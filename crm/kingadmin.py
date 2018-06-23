# -*- coding: utf-8 -*-
# crm/kingadmin.py


from crm import models
from common import admin_base

# from kingadmin.sites import site

print('crm kingadmin....')


# 注册model
class CustomerAdmin(admin_base.BaseKingAdmin):
#class CustomerAdmin():
    list_display = ['name', 'source', 'contact_type', 'contact', 'consultant', 'consult_content', 'status', 'date']
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = ['contact', 'consultant__name']


customModel = models.CustomerInfo


def get_admin_and_model():
    return CustomerAdmin, [customModel, models.Role, models.Menus]

# site.register(models.CustomerInfo,CustomerAdmin)