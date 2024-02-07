from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.utils.functional import lazy

from easyhome.sso.views import index_page, login_page

admin.site.enable_nav_sidebar = False
admin.site.index_title = lazy(lambda: f"EasyHome Admin. Release: {settings.RELEASE}", str)()

urlpatterns = [
    path("", index_page),
    path("login/", login_page),
    path("logout/", LogoutView.as_view()),
    path("easyhome/", admin.site.urls),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)), *urlpatterns]
