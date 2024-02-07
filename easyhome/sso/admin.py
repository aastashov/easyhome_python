from __future__ import annotations  # noqa: D100

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import site as default_site
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.utils.functional import lazy

from easyhome.sso.forms import AdminAuthenticationForm


class AdminSite(admin.AdminSite):  # noqa: D101
    login_form = AdminAuthenticationForm
    login_template = "admin/login.html"

    def _registry_getter(self):  # noqa: ANN202
        return default_site._registry  # noqa: SLF001

    def _registry_setter(self, value) -> None:  # noqa: ANN001
        default_site._registry = value  # noqa: SLF001

    _registry = property(_registry_getter, _registry_setter)


def _get_index_title() -> str:
    return f"EasyHome Admin. Release: {settings.RELEASE}"


site = AdminSite()
site.enable_nav_sidebar = False
admin.site = site
default_site.enable_nav_sidebar = False
default_site.index_title = lazy(_get_index_title, str)()

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
