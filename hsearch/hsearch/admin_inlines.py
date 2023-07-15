from django.contrib import admin
from django.db import models
from django.forms import Widget
from django.http import HttpRequest
from django.utils.safestring import SafeString

from hsearch.hsearch.models import Answer, Feedback, Image


class BaseReadOnly(admin.TabularInline):
    extra = 0
    classes = [
        "collapse",
    ]

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request, obj) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class AdminImageWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None) -> SafeString:
        display_name = value.split("/")[-1]
        img = f'<img height="200px" src="{value}" alt="{display_name}"/>'
        return SafeString(f'<a href="{value}" target="_blank">{img}</a>')


class FeedbackInline(BaseReadOnly):
    model = Feedback
    fields = [
        "body",
        "created",
    ]


class AnswerInline(BaseReadOnly):
    model = Answer
    fields = [
        "apartment",
        "dislike",
        "created",
    ]


class ImageInline(BaseReadOnly):
    model = Image
    fields = [
        "path",
        "created",
    ]
    readonly_fields = [
        "created",
    ]
    formfield_overrides = {models.CharField: {"widget": AdminImageWidget}}

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return True
