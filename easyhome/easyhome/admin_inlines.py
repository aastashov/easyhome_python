from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from django.contrib import admin
from django.db import models
from django.forms import Widget
from django.utils.safestring import SafeString

from easyhome.easyhome.models import Answer, Feedback, Image

if TYPE_CHECKING:
    from django.http import HttpRequest


class BaseReadOnly(admin.TabularInline):  # noqa: D101
    extra = 0
    classes = (
        "collapse",
    )

    def has_delete_permission(self, request, obj=None) -> bool:  # noqa: ANN001, D102
        return False

    def has_add_permission(self, request, obj) -> bool:  # noqa: ANN001, D102
        return False

    def has_change_permission(self, request, obj=None) -> bool:  # noqa: ANN001, D102
        return False


class AdminImageWidget(Widget):  # noqa: D101
    def render(self, name, value, attrs=None, renderer=None) -> SafeString:  # noqa: ANN001, D102
        display_name = value.split("/")[-1]
        img = f'<img height="200px" src="{value}" alt="{display_name}"/>'
        return SafeString(f'<a href="{value}" target="_blank">{img}</a>')


class FeedbackInline(BaseReadOnly):  # noqa: D101
    model = Feedback
    fields = (
        "body",
        "created",
    )


class AnswerInline(BaseReadOnly):  # noqa: D101
    model = Answer
    fields = (
        "apartment",
        "dislike",
        "created",
    )


class ImageInline(BaseReadOnly):  # noqa: D101
    model = Image
    fields = (
        "path",
        "created",
    )
    readonly_fields = (
        "created",
    )
    formfield_overrides = {models.CharField: {"widget": AdminImageWidget}}  # noqa: RUF012

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:  # noqa: ANN001, D102
        return True
