from __future__ import annotations  # noqa: D100

from typing import TYPE_CHECKING

from django_filters import FilterSet
from django_filters.filters import CharFilter, DateTimeFilter
from graphene import DateTime
from graphene_django.converter import convert_django_field

from easyhome.easyhome.models import Apartment, Image
from unixtimestampfield.fields import UnixTimeStampField

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from graphene_django.registry import Registry


@convert_django_field.register(UnixTimeStampField)
def convert_field_to_string(field: UnixTimeStampField, _: Registry | None = None) -> DateTime:
    """Use this function to convert the UnixTimeStampField to a DateTime graphene field."""
    return DateTime(description=field.help_text, required=not field.null)


class ApartmentFilter(FilterSet):
    """Use this class to filter the Apartment model."""

    created = DateTimeFilter()
    topic_icontains = CharFilter(method="filter_topic_icontains")
    phone = CharFilter(lookup_expr="istartswith")
    body = CharFilter(lookup_expr="icontains")
    site = CharFilter(field_name="site", lookup_expr="iexact")

    def filter_topic_icontains(self, queryset: QuerySet[Apartment], name: str, value: str) -> QuerySet[Apartment]:
        """Use this method to filter the topic field by the icontains lookup."""
        return queryset.filter(topic__icontains=value)

    class Meta:
        """Metaclass for the ApartmentFilter."""

        model = Apartment
        fields = (
            "id",
            "external_id",
            "url",
            "topic",
            "phone",
            "rooms",
            "body",
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
            "images_count",
            "is_deleted",
            "created",
        )


class ImageFilter(FilterSet):
    """Use this class to filter the Image model."""

    created = DateTimeFilter()

    class Meta:
        """Metaclass for the ImageFilter."""

        model = Image
        fields = (
            "id",
            "apartment",
            "path",
            "created",
        )
