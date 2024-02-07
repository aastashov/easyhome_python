from __future__ import annotations  # noqa: D100

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


def index_page(request):  # noqa: ANN001, ANN201, D103
    context = {
        "bot_name": settings.TG_NAME,
        "auth_url": f"{request.scheme}://{request.get_host()}{settings.TG_LOGIN_REDIRECT_URL}",
    }
    return render(request, "index.html", context=context)


def login_page(request):  # noqa: ANN001, ANN201, D103
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
