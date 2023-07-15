from django.contrib import admin


class BaseReadOnly(admin.TabularInline):
    extra = 0
    classes = [
        "collapse",
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


def yes_no_img(var):
    res = ("yes", "True") if var else ("no", "False")
    return '<img src="/static/admin/img/icon-{}.svg" alt="{}">'.format(*res)
