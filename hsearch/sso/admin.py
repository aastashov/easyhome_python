from django.contrib import admin
from django.contrib.admin.sites import site as default_site
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from hsearch.sso.forms import AdminAuthenticationForm


class AdminSite(admin.AdminSite):
    login_form = AdminAuthenticationForm
    login_template = "admin/login.html"

    def _registry_getter(self):
        return default_site._registry

    def _registry_setter(self, value):
        default_site._registry = value

    _registry = property(_registry_getter, _registry_setter)


site = AdminSite()
site.enable_nav_sidebar = False
admin.site = site
default_site.enable_nav_sidebar = False

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
