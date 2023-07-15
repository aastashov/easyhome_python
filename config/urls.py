from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from hsearch.api.router import api_v1
from hsearch.common.admin import admin
from hsearch.sso.views import index_page, login_page

admin.autodiscover()

urlpatterns = [
    path("", index_page),
    path("login/", login_page),
    path("logout/", LogoutView.as_view()),
    path("auth/", include("social_django.urls", namespace="social")),
    path("hsearch/", admin.site.urls),
    path("api/v1/", api_v1.urls),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
