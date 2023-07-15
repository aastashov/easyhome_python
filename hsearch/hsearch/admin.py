from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import SafeString

from hsearch.common.admin import yes_no_img
from hsearch.hsearch.admin_inlines import AnswerInline, FeedbackInline, ImageInline
from hsearch.hsearch.models import Answer, Apartment, Chat, Feedback, Image, TgMessage


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        "display",
        "telegram_link",
        "c_type",
        "sites",
        "other_filters",
        "enable",
        "created",
    ]

    list_filter = [
        "c_type",
        "enable",
        "diesel",
        "lalafo",
        "house",
        "photo",
    ]

    search_fields = [
        "title",
        "username",
    ]

    inlines = [
        FeedbackInline,
        AnswerInline,
    ]

    ordering = [
        "-created",
    ]

    @admin.display(description="Display")
    def display(self, obj: Chat) -> str:
        return f"{obj.title} (#{obj.pk})"

    @admin.display(description="Telegram")
    def telegram_link(self, obj: Chat) -> SafeString:
        if not obj.username:
            return SafeString("-")
        return SafeString(f'<a href="https://t.me/{obj.username}">{obj.username}</a>')

    @admin.display(description="Sites")
    def sites(self, obj: Chat) -> SafeString:
        return SafeString(
            f"diesel: {yes_no_img(obj.diesel)}<br>"
            f"lalafo: {yes_no_img(obj.lalafo)}<br>"
            f"house: {yes_no_img(obj.house)}",
        )

    @admin.display(description="Other filters")
    def other_filters(self, obj: Chat) -> SafeString:
        return SafeString(f"usd: {obj.usd}<br>" f"kgs: {obj.kgs}<br>" f"photo: {yes_no_img(obj.photo)}<br>")


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    search_fields = [
        "topic",
        "body",
    ]

    list_display = [
        "url",
        "topic",
        "phone",
        "rooms",
        "body",
        "images_count",
        "price",
        "currency",
        "area",
        "city",
        "room_type",
        "site",
        "floor",
        "max_floor",
        "district",
        "lat",
        "lon",
        "created",
    ]

    list_filter = [
        "site",
        "rooms",
        "currency",
        "floor",
    ]

    readonly_fields = [
        "images_count",
    ]

    inlines = [
        ImageInline,
    ]

    ordering = [
        "-created",
    ]

    phones_cache = {}

    def get_queryset(self, request: HttpRequest) -> QuerySet[Apartment]:
        qs = super().get_queryset(request)
        res = qs.values("phone").annotate(models.Count("pk")).order_by()
        self.phones_cache = {i["phone"]: i["pk__count"] for i in res}
        return qs

    @admin.display(description="Site")
    def site_link(self, obj: Apartment) -> SafeString:
        return SafeString(f'<a href="{obj.url}" target="_blank">{obj.site.title()}</a>')

    @admin.display(description="Phone")
    def phone_count(self, obj: Apartment) -> SafeString:
        if obj.phone == "":
            return SafeString("-")
        phone_count = self.phones_cache.get(obj.phone) or 0
        if phone_count < 3:
            return SafeString(f'<a href="tel:{obj.phone}">{obj.phone}</a>')
        return SafeString(f'<a href="tel:{obj.phone}" style="color:red;">{obj.phone} ({phone_count})</a>')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "chat_link",
        "apartment_link",
        "dislike",
        "created",
    ]

    ordering = [
        "-created",
    ]

    @admin.display(description="Chat")
    def chat_link(self, obj: Answer) -> SafeString:
        return SafeString(f'<a href="/hsearch/hsearch/chat/{obj.chat.pk}/">{obj.chat}</a>')

    @admin.display(description="Apartment")
    def apartment_link(self, obj: Answer) -> SafeString:
        return SafeString(f'<a href="/hsearch/hsearch/apartment/{obj.apartment.pk}/">{obj.apartment}</a>')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "chat_link",
        "telegram_link",
        "body",
        "created",
    ]

    search_fields = [
        "username",
        "chat__title",
        "body",
    ]

    ordering = [
        "-created",
    ]

    @admin.display(description="Telegram")
    def telegram_link(self, obj: Feedback) -> SafeString:
        if not obj.username:
            return SafeString("-")
        return SafeString(f'<a href="https://t.me/{obj.username}">{obj.username}</a>')

    @admin.display(description="Chat")
    def chat_link(self, obj: Feedback) -> SafeString:
        return SafeString(f'<a href="/hsearch/hsearch/chat/{obj.chat.pk}/">{obj.chat}</a>')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "path",
        "apartment_link",
        "image",
        "created",
    ]

    autocomplete_fields = [
        "apartment",
    ]

    search_fields = [
        "apartment__topic",
        "path",
    ]

    ordering = [
        "-created",
    ]

    @admin.display(description="Image")
    def image(self, obj: Image) -> SafeString:
        name = obj.path.split("/")[-1]
        return SafeString(f'<img height="200px" src="{obj.path}" alt="{name}"/>')

    @admin.display(description="Apartment")
    def apartment_link(self, obj: Image) -> SafeString:
        return SafeString(f'<a href="/hsearch/hsearch/apartment/{obj.apartment.pk}/">{obj.apartment}</a>')


@admin.register(TgMessage)
class TgMessageAdmin(admin.ModelAdmin):
    list_display = [
        "message_id",
        "chat_link",
        "apartment_link",
        "kind",
        "created",
    ]

    autocomplete_fields = [
        "apartment",
        "chat",
    ]

    list_filter = [
        "kind",
    ]

    search_fields = [
        "chat__title",
        "apartment__topic",
    ]

    ordering = [
        "-created",
    ]

    @admin.display(description="Chat")
    def chat_link(self, obj: TgMessage) -> SafeString:
        return SafeString(f'<a href="/hsearch/hsearch/chat/{obj.chat.pk}/">{obj.chat}</a>')

    @admin.display(description="Apartment")
    def apartment_link(self, obj: TgMessage) -> SafeString:
        return SafeString(f'<a href="/hsearch/hsearch/apartment/{obj.apartment.pk}/">{obj.apartment}</a>')
