from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI

from hsearch.api.v1.handlers import apartment, profile
from hsearch.api.v1.handlers.profile import AuthFailed, AuthMissingParameter

api_v1 = NinjaAPI(
    version="1.0.0",
    title="House Search API",
    docs_decorator=staff_member_required,
)

api_v1.add_router("/apartment", apartment.router)
api_v1.add_router("/profile", profile.router)


@api_v1.exception_handler(AuthFailed)
def auth_failed(request: HttpRequest, exc: Exception) -> HttpResponse:
    return api_v1.create_response(request, {"message": str(exc)}, status=401)


@api_v1.exception_handler(AuthMissingParameter)
def auth_missing_parameter(request: HttpRequest, exc: Exception) -> HttpResponse:
    return api_v1.create_response(request, {"message": str(exc)}, status=400)
