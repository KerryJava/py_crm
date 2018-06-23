class BaseKingAdmin(object):
    model = None
    filter_conditions = []
    list_display = []
    list_filter = []
    filter_horizontal = []
    readonly_fields = []
    search_fields = []
    search_key = None

pass
