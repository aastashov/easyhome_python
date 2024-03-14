from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest


def index_page(request: HttpRequest) -> HttpResponse:
    """Use this view to render the index page."""
    context = {
        "bot_name": settings.TG_NAME,
        "auth_url": f"{request.scheme}://{request.get_host()}{settings.TG_LOGIN_REDIRECT_URL}",
    }
    return render(request, "index.html", context=context)


def login_page(request: HttpRequest) -> JsonResponse:
    """Use this view to log in the user."""
    if request.user.is_authenticated:
        return JsonResponse(
            data={
                "id": request.user.id,
                "username": request.user.username,
            },
        )
    return JsonResponse(
        data={
            "bot_name": settings.TG_NAME,
            "auth_url": f"{request.scheme}://{request.get_host()}{settings.TG_LOGIN_REDIRECT_URL}",
        },
        status=403,
    )
