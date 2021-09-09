from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


def index_page(request):
    return render(request, "index.html", context={
        "bot_name": settings.TG_NAME,
        "auth_url": f"{request.scheme}://{request.get_host()}{settings.TG_LOGIN_REDIRECT_URL}",
    })


def login_page(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "id": request.user.id,
            "username": request.user.username,
        })
    return JsonResponse({
        "bot_name": settings.TG_NAME,
        "auth_url": f"{request.scheme}://{request.get_host()}{settings.TG_LOGIN_REDIRECT_URL}",
    }, status=403)
