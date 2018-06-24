# -*- coding: utf-8 -*-
import json
from django.shortcuts import render

class BaseKingAdmin(object):

    def __init__(self):
        origin_list = self.actions
        origin_list.extend(self.default_actions)
        self.actions = list(set(origin_list))
        # self.actions.extend(list(set(self.default_actions)))

    model = None
    filter_conditions = []
    list_display = []
    list_filter = []
    filter_horizontal = []
    readonly_fields = []
    search_fields = []
    search_key = None
    list_per_page = 5
    actions = []
    default_actions = ['delete_selected_objs']

    def delete_selected_objs(self, request, querysets):
        querysets_ids = json.dumps([i.id for i in querysets])

        print("querysets_ids")
        print(querysets_ids)
        return render(request, 'kingadmin/table_obj_delete.html', {'admin_class': self,  # self就是admin_class
                                                                   'objs': querysets,
                                                                   'querysets_ids': querysets_ids
                                                                   })


pass
