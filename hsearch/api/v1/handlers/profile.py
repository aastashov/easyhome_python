import hashlib
import hmac
import json
import time
from dataclasses import dataclass

from django.conf import settings
from django.http import HttpRequest
from ninja import Router
from social_core.exceptions import AuthFailed, AuthMissingParameter

from hsearch.api.v1 import schemas
from hsearch.hsearch.models import Chat

router = Router(tags=["Profile"])


@dataclass
class TelegramUser:
    id: int
    username: str
    first_name: str
    last_name: str
    photo_url: str
    auth_date: int
    hash: str

    @property
    def fillname(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def data_check_string(self) -> str:
        return (
            f"auth_date={self.auth_date}\n"
            f"first_name={self.first_name}\n"
            f"id={self.id}\n"
            f"last_name={self.last_name}\n"
            f"photo_url={self.photo_url}\n"
            f"username={self.username}"
        )


def auth_user(request: HttpRequest) -> TelegramUser:
    telegram_user = TelegramUser(**json.loads(request.body))
    received_hash_string = telegram_user.hash
    auth_date = telegram_user.auth_date

    if received_hash_string is None or auth_date is None:
        raise AuthMissingParameter("telegram", "hash or auth_date")

    data_check_string = telegram_user.data_check_string
    secret_key = hashlib.sha256(settings.TG_TOKEN.encode()).digest()
    built_hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    current_timestamp = int(time.time())
    auth_timestamp = int(auth_date)
    if current_timestamp - auth_timestamp > 86400:
        raise AuthFailed("telegram", "Auth date is outdated")
    if built_hash != received_hash_string:
        raise AuthFailed("telegram", "Invalid hash supplied")

    return telegram_user


@router.post(
    "/settings",
    response=schemas.ProfileSettingsResponse,
    summary="Returns profile settings.",
)
def settings_view(request: HttpRequest) -> schemas.ProfileSettingsResponse:
    user = auth_user(request)
    chat, _ = Chat.objects.get_or_create(
        username=user.username,
        defaults={
            "username": user.username,
            "title": user.fillname,
            "created": int(time.time()),
        },
    )
    return chat
