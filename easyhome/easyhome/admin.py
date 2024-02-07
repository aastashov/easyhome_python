from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from django.contrib import admin
from django.db import models
from django.utils.safestring import SafeString

from easyhome.common.admin import yes_no_img
from easyhome.easyhome.admin_inlines import AnswerInline, FeedbackInline, ImageInline
from easyhome.easyhome.models import Answer, Apartment, Chat, Feedback, Image, TgMessage

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = [  # noqa: RUF012
        "display",
        "telegram_link",
        "c_type",
        "sites",
        "other_filters",
        "enable",
        "created",
    ]

    list_filter = [  # noqa: RUF012
        "c_type",
        "enable",
        "diesel",
        "lalafo",
        "house",
        "photo",
    ]

    search_fields = [  # noqa: RUF012
        "title",
        "username",
    ]

    inlines = [  # noqa: RUF012
        FeedbackInline,
        AnswerInline,
    ]

    ordering = [  # noqa: RUF012
        "-created",
    ]

    @admin.display(description="Display")
    def display(self, obj: Chat) -> str:  # noqa: D102
        return f"{obj.title} (#{obj.pk})"

    @admin.display(description="Telegram")
    def telegram_link(self, obj: Chat) -> SafeString:  # noqa: D102
        if not obj.username:
            return SafeString("-")
        return SafeString(f'<a href="https://t.me/{obj.username}">{obj.username}</a>')

    @admin.display(description="Sites")
    def sites(self, obj: Chat) -> SafeString:  # noqa: D102
        return SafeString(
            f"diesel: {yes_no_img(obj.diesel)}<br>"
            f"lalafo: {yes_no_img(obj.lalafo)}<br>"
            f"house: {yes_no_img(obj.house)}",
        )

    @admin.display(description="Other filters")
    def other_filters(self, obj: Chat) -> SafeString:  # noqa: D102
        return SafeString(f"usd: {obj.usd}<br>kgs: {obj.kgs}<br>photo: {yes_no_img(obj.photo)}<br>")


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):  # noqa: D101
    search_fields = [  # noqa: RUF012
        "topic",
        "body",
        "phone",
        "url",
    ]

    list_display = [  # noqa: RUF012
        "id",
        "phone",
        "price",
        "is_deleted",
        "url",
        "topic",
        "rooms",
        "body",
        "images_count",
        "currency",
        "area",
        "city",
        "room_type",
        "site",
        "floor",
        "max_floor",
        "district",
        "created",
    ]

    list_filter = [  # noqa: RUF012
        "site",
        "city",
        "currency",
    ]

    readonly_fields = [  # noqa: RUF012
        "images_count",
        "created",
    ]

    inlines = [  # noqa: RUF012
        ImageInline,
    ]

    ordering = [  # noqa: RUF012
        "-created",
    ]

    phones_cache = {}  # noqa: RUF012

    def get_queryset(self, request: HttpRequest) -> QuerySet[Apartment]:  # noqa: D102
        qs = super().get_queryset(request)
        res = qs.values("phone").annotate(models.Count("pk")).order_by()
        self.phones_cache = {i["phone"]: i["pk__count"] for i in res}
        return qs

    @admin.display(description="Site")
    def site_link(self, obj: Apartment) -> SafeString:  # noqa: D102
        return SafeString(f'<a href="{obj.url}" target="_blank">{obj.site.title()}</a>')

    @admin.display(description="Phone")
    def phone_count(self, obj: Apartment) -> SafeString:  # noqa: D102
        if obj.phone == "":
            return SafeString("-")
        phone_count = self.phones_cache.get(obj.phone) or 0
        if phone_count < 3:  # noqa: PLR2004
            return SafeString(f'<a href="tel:{obj.phone}">{obj.phone}</a>')
        return SafeString(f'<a href="tel:{obj.phone}" style="color:red;">{obj.phone} ({phone_count})</a>')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = [  # noqa: RUF012
        "pk",
        "chat_link",
        "apartment_link",
        "dislike",
        "created",
    ]

    readonly_fields = ("created",)

    ordering = (
        "-created",
    )

    @admin.display(description="Chat")
    def chat_link(self, obj: Answer) -> SafeString:  # noqa: D102
        return SafeString(f'<a href="/easyhome/easyhome/chat/{obj.chat.pk}/">{obj.chat}</a>')

    @admin.display(description="Apartment")
    def apartment_link(self, obj: Answer) -> SafeString:  # noqa: D102
        return SafeString(f'<a href="/easyhome/easyhome/apartment/{obj.apartment.pk}/">{obj.apartment}</a>')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = [  # noqa: RUF012
        "pk",
        "chat_link",
        "telegram_link",
        "body",
        "created",
    ]

    search_fields = [  # noqa: RUF012
        "username",
        "chat__title",
        "body",
    ]

    ordering = [  # noqa: RUF012
        "-created",
    ]

    @admin.display(description="Telegram")
    def telegram_link(self, obj: Feedback) -> SafeString:  # noqa: D102
        if not obj.username:
            return SafeString("-")
        return SafeString(f'<a href="https://t.me/{obj.username}">{obj.username}</a>')

    @admin.display(description="Chat")
    def chat_link(self, obj: Feedback) -> SafeString:  # noqa: D102
        return SafeString(f'<a href="/easyhome/easyhome/chat/{obj.chat.pk}/">{obj.chat}</a>')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = [  # noqa: RUF012
        "path",
        "apartment_link",
        "image",
        "created",
    ]

    autocomplete_fields = [  # noqa: RUF012
        "apartment",
    ]

    search_fields = [  # noqa: RUF012
        "apartment__topic",
        "path",
    ]

    ordering = [  # noqa: RUF012
        "-created",
    ]

    @admin.display(description="Image")
    def image(self, obj: Image) -> SafeString:  # noqa: D102
        name = obj.path.split("/")[-1]
        return SafeString(f'<img height="200px" src="{obj.path}" alt="{name}"/>')

    @admin.display(description="Apartment")
    def apartment_link(self, obj: Image) -> SafeString:  # noqa: D102
        return SafeString(f'<a href="/easyhome/easyhome/apartment/{obj.apartment.pk}/">{obj.apartment}</a>')


@admin.register(TgMessage)
class TgMessageAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = [  # noqa: RUF012
        "message_id",
        "chat_link",
        "apartment_link",
        "kind",
        "created",
    ]

    autocomplete_fields = [  # noqa: RUF012
        "apartment",
        "chat",
    ]

    list_filter = [  # noqa: RUF012
        "kind",
    ]

    search_fields = [  # noqa: RUF012
        "chat__title",
        "apartment__topic",
    ]

    ordering = [  # noqa: RUF012
        "-created",
    ]

    @admin.display(description="Chat")
    def chat_link(self, obj: TgMessage) -> SafeString:  # noqa: D102
        return SafeString(f'<a href="/easyhome/easyhome/chat/{obj.chat.pk}/">{obj.chat}</a>')

    @admin.display(description="Apartment")
    def apartment_link(self, obj: TgMessage) -> SafeString:  # noqa: D102
        return SafeString(f'<a href="/easyhome/easyhome/apartment/{obj.apartment.pk}/">{obj.apartment}</a>')
